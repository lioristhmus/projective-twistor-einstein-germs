-- Preserve preview-friendly blank lines around display math in Markdown while
-- restoring the surrounding prose to one logical paragraph in LaTeX output.

local joined_displays = 0

local function is_display_math(inline)
  if inline.t == "Math" then
    return inline.mathtype == "DisplayMath"
  end

  if inline.t == "Span" and #inline.content == 1 then
    if inline.identifier and inline.identifier:match("^eq:") then
      return true
    end
    return is_display_math(inline.content[1])
  end

  return false
end

local function is_display_paragraph(block)
  if block.t ~= "Para" and block.t ~= "Plain" then
    return false
  end

  if #block.content == 1 and is_display_math(block.content[1]) then
    return true
  end

  -- pandoc-crossref represents numbered equations as an equation environment
  -- split across RawInline nodes, with the labeled formula between them.
  local first = block.content[1]
  local last = block.content[#block.content]
  return first ~= nil
      and last ~= nil
      and first.t == "RawInline"
      and last.t == "RawInline"
      and first.text:match("^\\begin%{equation%*?%}") ~= nil
      and last.text:match("\\end%{equation%*?%}$") ~= nil
end

local function is_crossref_equation(block)
  return block.t == "RawBlock"
      and block.text:match("\\begin%{equation%*?%}") ~= nil
end

local function is_display_block(block)
  return is_display_paragraph(block) or is_crossref_equation(block)
end

local function is_prose_paragraph(block)
  return (block.t == "Para" or block.t == "Plain")
      and not is_display_paragraph(block)
end

local function display_inlines(block)
  if is_display_paragraph(block) then
    return block.content
  end

  return pandoc.Inlines({pandoc.RawInline("latex", block.text)})
end

local function append_inlines(target, source)
  target:insert(pandoc.SoftBreak())
  for _, inline in ipairs(source) do
    target:insert(inline)
  end
end

local function join_blocks(blocks)
  local output = pandoc.Blocks({})
  local index = 1

  while index <= #blocks do
    local block = blocks[index]

    if is_display_block(block) then
      local previous = output[#output]
      local following = blocks[index + 1]
      local math = display_inlines(block)

      if previous and is_prose_paragraph(previous) then
        append_inlines(previous.content, math)
        joined_displays = joined_displays + 1

        if following and is_prose_paragraph(following) then
          append_inlines(previous.content, following.content)
          index = index + 1
        end
      elseif following and is_prose_paragraph(following) then
        local merged = pandoc.Inlines({})
        for _, inline in ipairs(math) do
          merged:insert(inline)
        end
        append_inlines(merged, following.content)
        output:insert(pandoc.Para(merged))
        joined_displays = joined_displays + 1
        index = index + 1
      else
        output:insert(block)
      end
    else
      output:insert(block)
    end

    index = index + 1
  end

  return output
end


-- Blocks is invoked for the document body and for nested block containers such
-- as list items.  This keeps Markdown list structure intact while applying the
-- same paragraph treatment to indented display equations.
function Blocks(blocks)
  return join_blocks(blocks)
end

function Pandoc(doc)
  if doc.meta.abstract ~= nil then
    doc.meta.abstract = pandoc.MetaBlocks(
      join_blocks(pandoc.Blocks(doc.meta.abstract))
    )
  end

  io.stderr:write(string.format(
    "join-display-paragraphs: joined %d displays\n",
    joined_displays
  ))
  return doc
end
