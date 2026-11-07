-- Catatan tabel/gambar: ::: {.catatan} ... ::: di bawah tabel.
-- Judul tabel dibuat pendek; penjelasan isi (singkatan, sumber, cara membaca)
-- ditulis di blok ini. Teks diawali "Catatan:" miring dan bercetak kecil.
function Div(el)
  if not el.classes:includes("catatan") then return nil end
  local pertama = el.content[1]
  if pertama and (pertama.t == "Para" or pertama.t == "Plain") then
    local awal = pandoc.utils.stringify(pertama):sub(1, 8)
    if awal ~= "Catatan:" then
      table.insert(pertama.content, 1, pandoc.Space())
      table.insert(pertama.content, 1, pandoc.Emph({pandoc.Str("Catatan:")}))
    end
  end
  if FORMAT:match("latex") then
    local isi = {pandoc.RawBlock("latex", "\\begingroup\\small\\noindent")}
    for _, b in ipairs(el.content) do table.insert(isi, b) end
    table.insert(isi, pandoc.RawBlock("latex", "\\par\\endgroup\\medskip"))
    return isi
  elseif FORMAT:match("docx") then
    el.attributes["custom-style"] = "Catatan"
    return el
  end
  return el.content
end
