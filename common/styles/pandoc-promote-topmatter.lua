-- Promote the repository's plain-Markdown title block to Pandoc metadata.
-- This leaves the source readable in chat and Markdown preview while allowing
-- document classes such as amsart to build proper title and running-head data.

local function inlines_from_text(text)
  local parsed = pandoc.read(text, "markdown")
  if #parsed.blocks == 0 then
    return pandoc.Inlines({})
  end
  return parsed.blocks[1].content
end

local function latex_from_text(text)
  local inlines = inlines_from_text(text)
  local rendered = pandoc.write(
    pandoc.Pandoc({pandoc.Plain(inlines)}),
    "latex"
  )
  return rendered:gsub("%s+$", "")
end

local function shorten_title(title)
  title = title:gsub("%s+", " ")
  if utf8.len(title) <= 58 then
    return title
  end

  -- Prefer the mathematical subject after phrases such as "... of the ...".
  local subject = title:match("^[Aa] .- [Oo]f the (.+)$")
  if subject and utf8.len(subject) <= 58 then
    return subject
  end

  local words = {}
  local length = 0
  for word in title:gmatch("%S+") do
    local next_length = length + utf8.len(word) + (#words > 0 and 1 or 0)
    if next_length > 54 then
      break
    end
    words[#words + 1] = word
    length = next_length
  end
  return table.concat(words, " ") .. "..."
end

local function is_empty_div(block)
  return block.t == "Div" and #block.content == 0
end

local function is_strong_only(block)
  if block.t ~= "Para" and block.t ~= "Plain" then
    return false
  end
  local found = false
  for _, inline in ipairs(block.content) do
    if inline.t == "Strong" then
      found = true
    elseif inline.t ~= "Space" and inline.t ~= "SoftBreak"
        and inline.t ~= "LineBreak" then
      return false
    end
  end
  return found
end

local function is_emph_only(block)
  if block.t ~= "Para" and block.t ~= "Plain" then
    return false
  end
  local found = false
  for _, inline in ipairs(block.content) do
    if inline.t == "Emph" then
      found = true
    elseif inline.t ~= "Space" and inline.t ~= "SoftBreak"
        and inline.t ~= "LineBreak" then
      return false
    end
  end
  return found
end

local function looks_like_author(text)
  local words = 0
  for _ in text:gmatch("%S+") do
    words = words + 1
  end
  return words >= 2
      and words <= 5
      and not text:match("%d")
      and not text:match("[%.:,;]")
      and not text:match("[—–]")
end

local function block_to_latex(block)
  return pandoc.write(pandoc.Pandoc({block}), "latex"):gsub("%s+$", "")
end

local function is_contents_command(block)
  return block.t == "RawBlock"
      and (block.format == "latex" or block.format == "tex")
      and block.text:match("^%s*\\tableofcontents%s*$") ~= nil
end

local function has_short_leading_abstract(blocks)
  if #blocks == 0
      or blocks[1].t ~= "Header"
      or blocks[1].level ~= 2
      or pandoc.utils.stringify(blocks[1]):lower() ~= "abstract" then
    return false
  end

  local text = {}
  for index = 2, #blocks do
    local block = blocks[index]
    if block.t == "HorizontalRule" or block.t == "Header"
        or is_empty_div(block) or is_contents_command(block) then
      break
    end
    text[#text + 1] = pandoc.utils.stringify(block)
  end
  return utf8.len(table.concat(text, " ")) <= 1600
end

function Pandoc(doc)
  local blocks = doc.blocks
  local leading_anchors = pandoc.Blocks({})
  local title_notes = {}
  local promoted_markdown_title = false

  while #blocks > 0 and is_empty_div(blocks[1]) do
    leading_anchors:insert(table.remove(blocks, 1))
  end

  if doc.meta.title == nil
      and #blocks > 0
      and blocks[1].t == "Header"
      and blocks[1].level == 1 then
    doc.meta.title = pandoc.MetaInlines(blocks[1].content)
    table.remove(blocks, 1)
    promoted_markdown_title = true
  end

  if doc.meta.subtitle == nil
      and #blocks > 0
      and is_emph_only(blocks[1]) then
    doc.meta.subtitle = pandoc.MetaInlines(blocks[1].content[1].content)
    table.remove(blocks, 1)
  end

  if #blocks > 0
      and (blocks[1].t == "Para" or blocks[1].t == "Plain") then
    local text = pandoc.utils.stringify(blocks[1])
    local author, date = text:match(
      "^Author%.%s*(.-)%s+Date%.%s*(.-)%s*$"
    )
    if author and author ~= "" then
      doc.meta.author = pandoc.MetaList({
        pandoc.MetaInlines(inlines_from_text(author))
      })
      if date and date ~= "" then
        doc.meta.date = pandoc.MetaInlines(inlines_from_text(date))
      end
      table.remove(blocks, 1)
    end
  end

  if doc.meta.author == nil
      and #blocks > 0
      and is_strong_only(blocks[1]) then
    local text = pandoc.utils.stringify(blocks[1])
    if looks_like_author(text) then
      doc.meta.author = pandoc.MetaList({
        pandoc.MetaInlines(blocks[1].content[1].content)
      })
      table.remove(blocks, 1)
    end
  end

  while #blocks > 0
      and (blocks[1].t == "Para" or blocks[1].t == "Plain")
      and (is_strong_only(blocks[1]) or blocks[1].content[1].t == "Strong") do
    title_notes[#title_notes + 1] = block_to_latex(table.remove(blocks, 1))
  end

  local abstract_anchors = pandoc.Blocks({})
  while #blocks > 0 and is_empty_div(blocks[1]) do
    abstract_anchors:insert(table.remove(blocks, 1))
  end

  if doc.meta.abstract == nil
      and #blocks > 0
      and has_short_leading_abstract(blocks) then
    table.remove(blocks, 1)
    local abstract_blocks = pandoc.Blocks({})
    while #blocks > 0
        and blocks[1].t ~= "HorizontalRule"
        and blocks[1].t ~= "Header"
        and not is_contents_command(blocks[1]) do
      abstract_blocks:insert(table.remove(blocks, 1))
    end
    if #abstract_blocks > 0 then
      doc.meta.abstract = pandoc.MetaBlocks(abstract_blocks)
    end
    if #blocks > 0 and blocks[1].t == "HorizontalRule" then
      table.remove(blocks, 1)
    end
  else
    -- Long leading abstracts stay in the page-breakable body. Use the same
    -- unnumbered section heading as References instead of a run-in subsection.
    if doc.meta.abstract == nil and #blocks > 0
        and blocks[1].t == "Header" and blocks[1].level == 2
        and pandoc.utils.stringify(blocks[1]):lower() == "abstract" then
      blocks[1] = pandoc.Div({
        pandoc.RawBlock("latex", "\\pandocabstractheading")
      }, blocks[1].attr)
    end
    for index = #abstract_anchors, 1, -1 do
      blocks:insert(1, abstract_anchors[index])
      abstract_anchors:remove(index)
    end
  end

  if doc.meta.author == nil and doc.meta["default-author"] ~= nil then
    doc.meta.author = pandoc.MetaList({
      pandoc.MetaInlines(
        inlines_from_text(pandoc.utils.stringify(doc.meta["default-author"]))
      )
    })
  end

  local front_blocks = pandoc.Blocks({})
  if doc.meta.title ~= nil and doc.meta.author ~= nil then
    local full_title = pandoc.utils.stringify(doc.meta.title)
    local full_author = pandoc.utils.stringify(doc.meta.author)
    local short_title = doc.meta["short-title"]
        and pandoc.utils.stringify(doc.meta["short-title"])
        or shorten_title(full_title)
    local short_author = doc.meta["short-author"]
        and pandoc.utils.stringify(doc.meta["short-author"])
        or full_author
    local running_heads = string.format(
      "\\markboth{\\MakeUppercase{%s}}{\\MakeUppercase{%s}}",
      latex_from_text(short_author),
      latex_from_text(short_title)
    )
    front_blocks:insert(pandoc.RawBlock("latex", running_heads))
  end

  for _, anchor in ipairs(leading_anchors) do
    front_blocks:insert(anchor)
  end
  for _, anchor in ipairs(abstract_anchors) do
    front_blocks:insert(anchor)
  end
  if #title_notes > 0 then
    front_blocks:insert(pandoc.RawBlock(
      "latex",
      "\\begin{center}\n"
        .. table.concat(title_notes, "\n\n")
        .. "\n\\end{center}"
    ))
  end
  for index = #front_blocks, 1, -1 do
    blocks:insert(1, front_blocks[index])
  end

  -- The repository's plain-Markdown convention reserves H1 for the title and
  -- writes body sections as H2. Once that title is promoted, restore H2 body
  -- headings to LaTeX section level without affecting YAML-title manuscripts.
  if promoted_markdown_title then
    for _, block in ipairs(blocks) do
      if block.t == "Header" and block.level > 1 then
        block.level = block.level - 1
      end
    end
  end

  doc.blocks = blocks
  return doc
end
