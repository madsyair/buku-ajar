-- Hanya untuk fikstur uji G-DOCX (buat_fikstur.py): meniru keterangan Quarto
-- di DOCX tanpa Quarto, yaitu paragraf "Gambar 1.1: ..." di dalam Div fig-/tbl-
-- menjadi RawInline(pPr ImageCaption), Str "Gambar", Str nbsp, Str "1.1",
-- Str ":", ... sehingga word-otomatis.lua dapat diuji dengan Pandoc saja.
function Div(d)
  if not (d.identifier:match("^fig%-") or d.identifier:match("^tbl%-")) then return nil end
  for _, b in ipairs(d.content) do
    local c = b.t == "Para" and b.content
    if c and c[1] and c[1].t == "Str" and (c[1].text == "Gambar" or c[1].text == "Tabel")
        and c[2] and c[2].t == "Space" and c[3] and c[3].t == "Str" then
      local no = c[3].text:match("^([%dA-Z.]+):$")
      if no then
        local baru = pandoc.Inlines({
          pandoc.RawInline("openxml", '<w:pPr><w:pStyle w:val="ImageCaption"/></w:pPr>'),
          pandoc.Str(c[1].text), pandoc.Str("\u{a0}"), pandoc.Str(no), pandoc.Str(":")})
        for i = 4, #c do baru:insert(c[i]) end
        b.content = baru
      end
    end
  end
  return d
end
