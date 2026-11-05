-- Keep labeled headline displays in an Abstract addressable but unnumbered.
-- Body equations remain available to pandoc-crossref in their original form.

local function abstract_equation(block)
  if block.t ~= "Para" or #block.content < 2 then
    return nil
  end

  local math = block.content[1]
  local label = block.content[#block.content]
  if math.t ~= "Math" or math.mathtype ~= "DisplayMath"
      or label.t ~= "Str" then
    return nil
  end

  local identifier = label.text:match("^%{#(eq:[A-Za-z0-9:-]+)%}$")
  if identifier == nil then
    return nil
  end

  local body = math.text:gsub("^%s+", ""):gsub("%s+$", "")

  return pandoc.RawBlock(
    "latex",
    string.format(
      "\\hypertarget{%s}{}\n\\begin{equation*}\n%s\n\\end{equation*}",
      identifier,
      body
    )
  )
end


function Pandoc(doc)
  if doc.meta.abstract ~= nil then
    local abstract = pandoc.Blocks(doc.meta.abstract)
    for index, block in ipairs(abstract) do
      local replacement = abstract_equation(block)
      if replacement ~= nil then
        abstract[index] = replacement
      end
    end
    doc.meta.abstract = pandoc.MetaBlocks(abstract)
  end

  local in_abstract = false
  local abstract_level = nil

  for index, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      local heading = pandoc.utils.stringify(block):lower()
      if heading == "abstract" then
        in_abstract = true
        abstract_level = block.level
      elseif in_abstract and block.level <= abstract_level then
        in_abstract = false
        abstract_level = nil
      end
    elseif in_abstract then
      local replacement = abstract_equation(block)
      if replacement ~= nil then
        doc.blocks[index] = replacement
      end
    end
  end

  return doc
end
