-- Pandoc silently ignores OpenType font metadata under pdfLaTeX.
-- Reject it rather than publishing a PDF with unintended fonts.
function Meta(meta)
  local unicode_font_keys = {
    "mainfont", "mainfontoptions", "mainfontfallback",
    "sansfont", "sansfontoptions", "sansfontfallback",
    "monofont", "monofontoptions", "monofontfallback",
    "mathfont", "mathfontoptions", "mathspec", "fontfamilies",
    "CJKmainfont", "CJKsansfont", "CJKmonofont", "CJKoptions",
    "luatexjapresetoptions", "luatexjafontspecoptions"
  }
  for _, key in ipairs(unicode_font_keys) do
    local value = meta[key]
    if value ~= nil and value ~= false and pandoc.utils.stringify(value) ~= "" then
      error("pdfLaTeX cannot honor '" .. key .. "'. Use --engine xelatex " ..
        "for OpenType fonts, or --profile ccg-jp for Japanese. No engine was switched.")
    end
  end
end
