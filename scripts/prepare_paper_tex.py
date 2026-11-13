#!/usr/bin/env python3
"""Conservative, logged layout repairs for generated Pandoc TeX, not Markdown."""

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


TOKEN = re.compile(r"%[^\n]*|\\(?:begin|end)\{[^}]+\}|\\[A-Za-z@]+|\\.|.", re.S)
MATH_ENVS = {"equation", "align", "alignat", "gather", "multline", "flalign", "displaymath", "math", "eqnarray"}
CODE_ENVS = {"verbatim", "Verbatim", "lstlisting", "minted", "Highlighting"}
FONT = re.compile(r"([_^])\s*(\\(?:mathbb|mathcal|mathrm|mathbf|mathfrak|mathscr|boldsymbol))(?![A-Za-z])\s*")


@dataclass
class MathRegion:
    start: int
    body_start: int
    body_end: int
    end: int
    kind: str


def protected_ranges(text):
    ranges = []
    ignore_until = 0
    for token in TOKEN.finditer(text):
        if token.start() < ignore_until:
            continue
        value = token.group()
        if value.startswith("%"):
            ranges.append((token.start(), token.end()))
        elif value.startswith(r"\begin{") and value[7:-1].rstrip("*") in CODE_ENVS:
            ending = r"\end{" + value[7:-1] + "}"
            end = text.find(ending, token.end())
            ignore_until = end + len(ending) if end >= 0 else len(text)
            ranges.append((token.start(), ignore_until))
        elif value in (r"\verb", r"\lstinline", r"\Verb"):
            pos = token.end() + (text[token.end():token.end() + 1] == "*")
            end = text.find(text[pos], pos + 1) if pos < len(text) else -1
            ignore_until = end + 1 if end >= 0 else len(text)
            ranges.append((token.start(), ignore_until))
    return ranges


def closing_group(text, start, opening="{", closing="}"):
    depth = 0
    for token in TOKEN.finditer(text, start):
        value = token.group()
        if value == opening:
            depth += 1
        elif value == closing:
            depth -= 1
            if depth == 0:
                return token.end()
    return None


def math_regions(text):
    regions = []
    ignore_until = 0
    for token in TOKEN.finditer(text):
        if token.start() < ignore_until:
            continue
        value = token.group()
        if value.startswith("%"):
            continue
        if value in (r"\verb", r"\lstinline", r"\Verb"):
            pos = token.end()
            if text[pos:pos + 1] == "*":
                pos += 1
            if pos < len(text):
                end = text.find(text[pos], pos + 1)
                ignore_until = end + 1 if end >= 0 else len(text)
            continue
        if value.startswith(r"\begin{"):
            name = value[7:-1]
            if name.rstrip("*") in CODE_ENVS:
                end = text.find(r"\end{" + name + "}", token.end())
                ignore_until = end + len(name) + 6 if end >= 0 else len(text)
                continue
            if name.rstrip("*") not in MATH_ENVS:
                continue
            ending = r"\end{" + name + "}"
            kind = name
        elif value in (r"\(", r"\["):
            ending = r"\)" if value == r"\(" else r"\]"
            kind = "inline" if value == r"\(" else "display"
        else:
            continue
        for end in TOKEN.finditer(text, token.end()):
            if end.group() == ending:
                regions.append(MathRegion(token.start(), token.end(), end.start(), end.end(), kind))
                ignore_until = end.end()
                break
    return regions


def top_positions(text, wanted, parens=True):
    braces = environments = left_right = parentheses = 0
    positions = []
    for token in TOKEN.finditer(text):
        value = token.group()
        if value.startswith("%"):
            continue
        if not (braces or environments or left_right or (parens and parentheses)) and value in wanted:
            positions.append((token.start(), token.end()))
        if value == "{":
            braces += 1
        elif value == "}":
            braces -= 1
        elif value.startswith(r"\begin{"):
            environments += 1
        elif value.startswith(r"\end{"):
            environments -= 1
        elif value == r"\left":
            left_right += 1
        elif value == r"\right":
            left_right -= 1
        elif value in ("(", "[", r"\langle", r"\lbrace", r"\lbrack", r"\lvert", r"\lVert"):
            parentheses += 1
        elif value in (")", "]", r"\rangle", r"\rbrace", r"\rbrack", r"\rvert", r"\rVert"):
            parentheses -= 1
    return positions


def split_at(text, positions):
    chunks = []
    previous = 0
    for start, end in positions:
        chunks.append(text[previous:start].strip())
        previous = end
    chunks.append(text[previous:].strip())
    return chunks


def core_range(body):
    start = 0
    metadata = re.compile(r"\s*(?:\\protect|\\phantomsection|\\label\{[^}]*\})")
    while match := metadata.match(body, start):
        start = match.end()
    while start < len(body) and body[start].isspace():
        start += 1
    end = len(body.rstrip())
    if body[start:start + 1] == "{" and closing_group(body, start) == end:
        return start + 1, end - 1
    return start, end


def fingerprint(text):
    text = re.sub(r"\\(?:begin|end)\{(?:aligned|gathered)\}", "", text)
    text = re.sub(r"\\(?:qquad|quad)(?![A-Za-z])|\\\\|&", "", text)
    return re.sub(r"\s+", "", text)


def repair_font_scripts(body):
    edits = []
    comments = [(m.start(), m.end()) for m in TOKEN.finditer(body) if m.group().startswith("%")]
    for match in FONT.finditer(body):
        if edits and match.start() < edits[-1][1]:
            continue
        if any(start <= match.start() < end for start, end in comments):
            continue
        start = match.end()
        if body[start:start + 1] == "{":
            end = closing_group(body, start)
        elif body[start:start + 1] == "\\":
            argument = re.match(r"\\[A-Za-z@]+|\\.", body[start:])
            end = start + argument.end() if argument else None
        else:
            end = start + 1 if start < len(body) and body[start].isalnum() else None
        if end:
            replacement = match.group(1) + "{" + body[match.start(2):end] + "}"
            edits.append((match.start(), end, replacement))
    return replace_ranges(body, edits), len(edits)


def split_tuple_row(row):
    alignment = top_positions(row, {"&"}, parens=False)
    if len(alignment) != 1:
        return None
    offset = alignment[0][1]
    right = row[offset:]
    opening = re.match(r"\s*=\s*(?:\\(?:bigl|Bigl))?\(", right)
    if not opening:
        return None
    paren = opening.end() - 1
    close = closing_group(right, paren, "(", ")")
    if not close or re.fullmatch(r"\s*[,.;]?\s*", right[close:]) is None:
        return None
    inside = right[paren + 1:close - 1]
    # A size command immediately before the final parenthesis belongs outside.
    size = re.search(r"\\(?:bigr|Bigr)\s*$", inside)
    suffix = ""
    if size:
        suffix, inside = inside[size.start():], inside[:size.start()]
    commas = top_positions(inside, {","})
    if not commas:
        return None
    parts = split_at(inside, commas)
    joined = (",\\\\\n &\\quad ").join(parts)
    return row[:offset] + right[:paren + 1] + joined + suffix + right[close - 1:]


def split_inner_delimiter(core):
    stack = []
    candidates = []
    for token in TOKEN.finditer(core):
        if token.group() == r"\left":
            delimiter = re.match(r"\s*(?:\\[{}]|[([])", core[token.end():])
            stack.append((token.end() + delimiter.end()) if delimiter else None)
        elif token.group() == r"\right" and stack:
            start = stack.pop()
            if start is not None:
                inside = core[start:token.start()]
                for separator in (r"\qquad", r"\quad"):
                    cuts = top_positions(inside, {separator})
                    if cuts:
                        rows = split_at(inside, cuts)
                        replacement = "\\begin{gathered}\n" + " \\\\\n".join(rows) + "\n\\end{gathered}"
                        candidates.append((len(inside), start, token.start(), replacement))
                        break
    if candidates:
        _, start, end, replacement = max(candidates)
        return core[:start] + replacement + core[end:]
    return None


def reflow_core(core):
    aligned = re.fullmatch(r"\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*", core, re.S)
    if aligned and not re.search(r"\\\\\s*\[", core):
        rows = split_at(aligned.group(1), top_positions(aligned.group(1), {r"\\"}, parens=False))
        result = []
        changed = False
        for row in rows:
            fields = split_at(row, top_positions(row, {"&"}, parens=False))
            if len(fields) >= 4 and len(fields) % 2 == 0:
                result.extend("&".join(fields[index:index + 2]) for index in range(0, len(fields), 2))
                changed = True
            else:
                result.append(row)
        if changed:
            return "\\begin{aligned}\n" + " \\\\\n".join(result) + "\n\\end{aligned}"
        tuples = [(len(row), index, split_tuple_row(row)) for index, row in enumerate(rows)]
        tuples = [item for item in tuples if item[2] is not None]
        if tuples:
            _, index, replacement = max(tuples)
            rows[index] = replacement
            return "\\begin{aligned}\n" + " \\\\\n".join(rows) + "\n\\end{aligned}"
        return None

    gathered = re.fullmatch(r"\s*\\begin\{gathered\}(.*?)\\end\{gathered\}\s*", core, re.S)
    if gathered:
        rows = split_at(gathered.group(1), top_positions(gathered.group(1), {r"\\"}, parens=False))
        for _, index in sorted(((len(row), index) for index, row in enumerate(rows)), reverse=True):
            replacement = reflow_core(rows[index])
            if replacement:
                rows[index] = replacement
                return "\\begin{gathered}\n" + " \\\\\n".join(rows) + "\n\\end{gathered}"
        return None

    for separator in (r"\qquad", r"\quad"):
        cuts = top_positions(core, {separator})
        if cuts:
            return "\\begin{gathered}\n" + " \\\\\n".join(split_at(core, cuts)) + "\n\\end{gathered}"
    inner = split_inner_delimiter(core)
    if inner:
        return inner
    relations = top_positions(core, {"=", "<", ">", r"\le", r"\ge", r"\leq", r"\geq", r"\simeq", r"\cong"})
    if len(relations) >= 2:
        separators = top_positions(core, {",", ";"})
        if any(relations[0][0] < start < relations[-1][0] for start, _ in separators):
            return None
        if any(not core[left[1]:right[0]].strip() for left, right in zip(relations, relations[1:])):
            return None
        first = relations[0][0]
        rows = [core[:first].strip() + "&" + core[first:relations[1][0]].strip()]
        for index in range(1, len(relations)):
            end = relations[index + 1][0] if index + 1 < len(relations) else len(core)
            rows.append("&" + core[relations[index][0]:end].strip())
        return "\\begin{aligned}\n" + " \\\\\n".join(rows) + "\n\\end{aligned}"
    return None


def replace_ranges(text, edits):
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def overfull_boxes(log, minimum=0):
    boxes = []
    pattern = r"Overfull \\hbox \(([\d.]+)pt too wide\) (detected at line|in paragraph at lines) (\d+)(?:--(\d+))?"
    for match in re.finditer(pattern, log):
        width = float(match.group(1))
        if width > minimum:
            boxes.append({"width_pt": width, "start_line": int(match.group(3)),
                          "end_line": int(match.group(4) or match.group(3)),
                          "display": match.group(2) == "detected at line"})
    return boxes



def place_ams_abstract(tex):
    """Move only Pandoc's adjacent AMS title/abstract pair to native order."""
    protected = protected_ranges(tex)
    classes = re.finditer(r"\\documentclass(?:\s*\[[^]]*\])?\s*\{([^}]+)\}", tex)
    document_class = next((m for m in classes
                           if not any(a <= m.start() < b for a, b in protected)), None)
    if document_class is None or document_class.group(1) != "amsart":
        return tex, False
    pattern = r"(\\begin\{document\}\s*)(\\maketitle[ \t]*\r?\n)([ \t]*\\begin\{abstract\})"
    match = re.search(pattern, tex)
    if not match:
        return tex, False
    if any(a <= match.start() < b for a, b in protected):
        return tex, False
    finish = None
    for token in TOKEN.finditer(tex, match.end()):
        if any(a <= token.start() < b for a, b in protected):
            continue
        if token.group() == r"\begin{abstract}":
            return tex, False
        if token.group() == r"\end{abstract}":
            finish = token.end()
            break
    if finish is None:
        return tex, False
    block = tex[match.start(3):finish]
    replacement = match.group(1) + block + "\n" + match.group(2)
    return tex[:match.start()] + replacement + tex[finish:], True

def normalize(tex):
    edits, events = [], []
    for region in math_regions(tex):
        repaired, count = repair_font_scripts(tex[region.body_start:region.body_end])
        if count:
            edits.append((region.body_start, region.body_end, repaired))
            events.append({"action": "group-font-script", "count": count,
                           "line": tex.count("\n", 0, region.start) + 1})
    protected = protected_ranges(tex)
    pattern = r"(\\begin\{CSLReferences\}\{[^}]*\}\{[^}]*\})(?!\s*\\sloppy\b)"
    count = 0
    for match in re.finditer(pattern, tex):
        if not any(start <= match.start() < end for start, end in protected):
            edits.append((match.start(), match.end(), match.group(1) + "\n\\sloppy"))
            count += 1
    result = replace_ranges(tex, edits)
    if count:
        events.append({"action": "bibliography-line-flexibility", "count": count})
    result, moved = place_ams_abstract(result)
    if moved:
        events.append({"action": "ams-abstract-before-title", "count": 1})
    return result, events


def reflow(tex, log, threshold):
    regions = math_regions(tex)
    edits, events, used = [], [], set()
    for box in overfull_boxes(log, threshold):
        candidates = []
        for region in regions:
            start = tex.count("\n", 0, region.start) + 1
            end = tex.count("\n", 0, region.end) + 1
            if start <= box["end_line"] and end >= box["start_line"]:
                if box["display"] != (region.kind != "inline"):
                    continue
                candidates.append(region)
        if not candidates:
            continue
        region = max(candidates, key=lambda item: item.body_end - item.body_start)
        if region.start in used:
            continue
        body = tex[region.body_start:region.body_end]
        if region.kind == "inline":
            if len(body) < 80 or box["width_pt"] <= 10:
                continue
            replacement = r"\[" + body + r"\]"
            edits.append((region.start, region.end, replacement))
            action = "display-long-inline-math"
        elif region.kind in ("equation", "equation*", "display"):
            start, end = core_range(body)
            replacement = reflow_core(body[start:end])
            if replacement is None:
                continue
            if fingerprint(body[start:end]) != fingerprint(replacement):
                raise ValueError("Reflow changed mathematical tokens; refusing to write TeX")
            edits.append((region.body_start + start, region.body_start + end, replacement))
            action = "wrap-display-math"
        else:
            continue
        used.add(region.start)
        events.append({"action": action, "line": box["start_line"], "width_pt": box["width_pt"]})
    result = replace_ranges(tex, edits)
    if re.findall(r"\\label\{[^}]+\}", result) != re.findall(r"\\label\{[^}]+\}", tex):
        raise ValueError("Reflow changed labels; refusing to write TeX")
    return result, events


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--latex-log", type=Path)
    parser.add_argument("--status-file", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--threshold", type=float, default=10.0)
    args = parser.parse_args()
    if args.tex.suffix != ".tex":
        parser.error("Only generated .tex files may be edited")
    tex = args.tex.read_text()
    report = json.loads(args.report.read_text()) if args.report.exists() else {"adjustments": []}
    log = args.latex_log.read_text(errors="replace") if args.latex_log else ""
    if args.check:
        warnings = overfull_boxes(log, args.threshold)
        report["remaining_overfull_boxes"] = overfull_boxes(log)
        report["undefined_references"] = "There were undefined references" in log
        report["missing_glyphs"] = "Missing character:" in log
        flagged = bool(warnings or report["undefined_references"] or report["missing_glyphs"])
        args.status_file.write_text("warnings\n" if flagged else "clean\n")
        print(f"TeX check: {len(warnings)} overfull boxes above {args.threshold:g}pt; "
              f"undefined references={report['undefined_references']}; missing glyphs={report['missing_glyphs']}")
    else:
        repaired, events = reflow(tex, log, args.threshold) if args.latex_log else normalize(tex)
        if repaired != tex:
            report.setdefault("original_tex_sha256", hashlib.sha256(tex.encode()).hexdigest())
            args.tex.write_text(repaired)
        report["adjustments"].extend(events)
        args.status_file.write_text("changed\n" if repaired != tex else "unchanged\n")
        print(f"TeX layout: {len(events)} adjustment(s)")
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
