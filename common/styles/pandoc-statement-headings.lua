-- Give numbered bold statement headings AMS-like spacing without guessing
-- where their bodies end or changing their manual numbering and body fonts.

local statement_names = {
  Definition = true,
  Theorem = true,
  Lemma = true,
  Proposition = true,
  Corollary = true,
  Remark = true,
  Example = true,
  Conjecture = true,
  Claim = true,
  Notation = true,
  Assumption = true,
  Observation = true,
  Fact = true,
}

local function is_statement_heading(inline)
  if inline == nil or inline.t ~= "Strong" then
    return false
  end

  local name, number = pandoc.utils.stringify(inline):match(
    "^(%a+)%s+([^%s]+)"
  )
  return statement_names[name] == true
      and (number:match("^%d") ~= nil
        or number:match("^%u+%.%d") ~= nil)
end

local function is_empty_anchor(block)
  return block ~= nil and block.t == "Div"
      and #block.content == 0 and block.identifier ~= ""
end

function Blocks(blocks)
  if not FORMAT:match("latex") then
    return nil
  end

  local output = pandoc.Blocks({})
  for _, block in ipairs(blocks) do
    if (block.t == "Para" or block.t == "Plain")
        and is_statement_heading(block.content[1]) then
      local anchors = pandoc.Blocks({})
      -- Keep preceding link targets on the heading's page after its top space.
      while is_empty_anchor(output[#output]) do
        anchors:insert(1, output:remove(#output))
      end
      local anchor_tex = pandoc.write(pandoc.Pandoc(anchors), "latex")
      local heading_tex = pandoc.write(pandoc.Pandoc({
        pandoc.Plain(block.content[1].content),
      }), "latex"):gsub("%s+$", "")
      output:insert(pandoc.RawBlock("latex",
        "\\pandocstatementheading{" .. anchor_tex .. heading_tex .. "}"
      ))

      local rest = pandoc.Inlines({})
      for index = 2, #block.content do
        local inline = block.content[index]
        if #rest > 0 or (inline.t ~= "Space" and inline.t ~= "SoftBreak"
            and inline.t ~= "LineBreak") then
          rest:insert(inline)
        end
      end
      if #rest > 0 then
        output:insert(pandoc.Para(rest))
      end
    else
      output:insert(block)
    end
  end
  return output
end
