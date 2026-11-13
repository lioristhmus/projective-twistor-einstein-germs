-- Run after citeproc so a heading is added only for an actual bibliography.

local function normalized(text)
  return text:gsub("%s+", " "):gsub("^%s+", ""):gsub("%s+$", ""):lower()
end

local function is_bibliography(block)
  return block.t == "Div" and #block.content > 0
      and block.classes:includes("references")
      and block.classes:includes("csl-bib-body")
end

local function heading_text(block)
  if block.t == "Header" then
    return pandoc.utils.stringify(block.content)
  end
  if block.t == "RawBlock" and (block.format == "latex" or block.format == "tex") then
    local command, title = block.text:match("^%s*\\(%a+)%*?%{(.-)%}")
    if command == "section" or command == "subsection" or command == "chapter" then
      return title
    end
  end
  return nil
end

function Pandoc(doc)
  local title = doc.meta["reference-section-title"]
      and pandoc.utils.stringify(doc.meta["reference-section-title"])
      or "References"
  if normalized(title) == "" then
    return doc:walk({Header = function(header)
      if header.identifier == "bibliography" and #header.content == 0 then
        return {}
      end
    end})
  end
  -- AMS starred sections already write their own table-of-contents entry.
  local heading_classes = {"unnumbered"}
  if FORMAT:match("latex") and doc.meta.documentclass
      and pandoc.utils.stringify(doc.meta.documentclass) == "amsart" then
    heading_classes[#heading_classes + 1] = "unlisted"
  end
  local parsed = pandoc.read(title, "markdown")
  local first = parsed.blocks[1]
  local title_inlines = first and (first.t == "Para" or first.t == "Plain" or first.t == "Header")
      and first.content or pandoc.Inlines({pandoc.Str(title)})
  local function previous_content(blocks, index)
    while index > 0 and blocks[index].t == "Div" and #blocks[index].content == 0 do
      index = index - 1
    end
    return index
  end

  local function has_heading(block)
    if block == nil then
      return false
    end
    return heading_text(block) ~= nil
  end

  return doc:walk({Blocks = function(blocks)
    local output = pandoc.Blocks({})
    for _, block in ipairs(blocks) do
      if is_bibliography(block) then
        local index = previous_content(output, #output)
        -- citeproc may create its own metadata-title heading after a manually
        -- supplied heading. Preserve the manual heading rather than duplicate it.
        if index > 0 and output[index].t == "Header" and output[index].identifier == "bibliography" then
          local before = previous_content(output, index - 1)
          if before > 0 and has_heading(output[before]) then
            output:remove(index)
            index = before
          end
        end
        if not has_heading(output[index]) then
          output:insert(pandoc.Header(1, title_inlines, pandoc.Attr("", heading_classes)))
        end
      end
      output:insert(block)
    end
    return output
  end})
end
