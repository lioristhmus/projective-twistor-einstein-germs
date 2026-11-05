-- Preserve empty manual bibliography anchors without making Pandoc emit
-- a standalone \bibitem outside a thebibliography environment.
function Div(div)
  if FORMAT:match("latex")
      and div.identifier:match("^ref%-")
      and #div.content == 0 then
    return pandoc.RawBlock(
      "latex",
      "\\hypertarget{" .. div.identifier .. "}{}"
    )
  end
end
