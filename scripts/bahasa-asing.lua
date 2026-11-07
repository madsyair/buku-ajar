-- Tandai frasa miring berbahasa asing sebagai bahasa Inggris (lang="en").
-- Dengan begitu babel (PDF) dan Word memenggalnya memakai pola Inggris,
-- bukan pola Indonesia. Daftar frasa dibangkitkan harness/penggalan.py.
local daftar = {}
local berkas = pandoc.path.join({pandoc.path.directory(PANDOC_SCRIPT_FILE),
                                 "istilah-asing.txt"})
local f = io.open(berkas, "r")
if f then
  for baris in f:lines() do
    if baris ~= "" and not baris:match("^#") then
      daftar[baris] = true
    end
  end
  f:close()
end

function Emph(el)
  if daftar[pandoc.utils.stringify(el)] then
    return pandoc.Span(el, {lang = "en"})
  end
end
