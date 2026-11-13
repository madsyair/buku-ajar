-- Sitasi Zotero "hidup" untuk keluaran DOCX seri Statistika Bayesian.
-- Hanya aktif bila FORMAT == "docx"; untuk PDF filter ini tidak berbuat apa-apa.
-- Dipasang di _quarto.yml sebagai filter "at: post-render" SESUDAH
-- word-otomatis.lua. Tidak memerlukan Zotero saat render (tidak memakai
-- zotero.lua dari Better BibTeX yang menghubungi Zotero yang sedang berjalan).
--
-- Cara kerja:
--   1. Filter Quarto "post-render" berjalan SEBELUM citeproc Pandoc, sehingga
--      filter ini menjalankan citeproc sendiri (pandoc.utils.citeproc) dengan
--      CSL, bahasa, dan link-citations yang sama. Rujukan silang Quarto
--      (@fig-, @tbl-, @eq-, @sec-) sudah selesai di tahap ini.
--   2. Setiap Cite menjadi bidang Word
--        { ADDIN ZOTERO_ITEM CSL_CITATION {json} }
--      dengan hasil bidang = teks citeproc (bertaut ke Daftar Pustaka), jadi
--      dokumen tetap terbaca tanpa Zotero. JSON memuat citationID,
--      properties (formattedCitation RTF, plainCitation, noteIndex),
--      citationItems (id, uris, itemData CSL-JSON dari pustaka.bib, locator,
--      label, prefix, suffix, suppress-author) dan schema csl-citation.json.
--      uris memakai URI Zotero tiruan ".../users/local/pustakabib/items/bib_<kunci>"
--      yang tidak pernah cocok dengan butir pustaka sungguhan (kunci Zotero
--      selalu huruf kapital), sehingga Zotero memakai itemData tersemat
--      (Zotero.Integration.Citation.loadItemData: tanpa uris kode Zotero
--      gagal pada citationItem.uris.length).
--   3. Sitasi naratif (@kunci) menjadi teks penulis biasa + bidang
--      bersuppress-author: "Mroz {(1987, hlm. 770)}" (Zotero tidak punya
--      mode naratif).
--   4. Div #refs menjadi bidang { ADDIN ZOTERO_BIBL {...} CSL_BIBLIOGRAPHY }
--      dengan hasil = Daftar Pustaka citeproc (bookmark ref-<kunci> tetap).
--   5. Preferensi dokumen Zotero (gaya CSL, bahasa, jenis bidang) ditulis ke
--      docProps/custom.xml sebagai ZOTERO_PREF_1, ZOTERO_PREF_2, ... (masing-
--      masing <= 255 karakter, seperti plugin Zotero untuk Word) lewat metadata
--      Pandoc; Pandoc menulis metadata sebagai properti kustom DOCX.
--   6. suppress-bibliography diset agar citeproc kedua (bawaan Pandoc) tidak
--      menambah apa pun; tidak ada Cite yang tersisa untuknya.
--
-- Matikan per buku dengan metadata `zotero-word: false`. Gaya Zotero dibaca
-- dari <id> berkas CSL (`csl:`); dapat ditimpa dengan `zotero-word-style:`.

if not FORMAT:match("docx") then return {} end

local SKEMA = "https://github.com/citation-style-language/schema/raw/master/csl-citation.json"
local URI_DASAR = "http://zotero.org/users/local/pustakabib/items/bib_"
local jumlah = {sitasi = 0, butir = 0, naratif = 0, tanpa_data = 0, bibl = 0}

local function esc(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

-- id acak tetapi deterministik (render ulang menghasilkan id yang sama)
local ALFABET = "23456789ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
local function id_acak(s, n)
  local h1, h2 = 5381, 52711
  for i = 1, #s do
    h1 = (h1 * 33 + s:byte(i)) % 2147483647
    h2 = (h2 * 31 + s:byte(i)) % 2147483629
  end
  local out = {}
  for i = 1, (n or 8) do
    local x = (h1 + h2 * i) % #ALFABET
    out[i] = ALFABET:sub(x + 1, x + 1)
    h1 = (h1 * 48271 + 11) % 2147483647
    h2 = (h2 * 69621 + 7) % 2147483629
  end
  return table.concat(out)
end

---------------------------------------------------------------- bidang
-- Kode bidang dipecah menjadi beberapa w:instrText (Word menyambungnya).
local function awal_bidang(instr)
  local runs = {'<w:r><w:fldChar w:fldCharType="begin"/></w:r>'}
  local kode = " " .. instr .. " "
  local i = 1
  while i <= #kode do
    local j = math.min(#kode, i + 1999)
    -- jangan memotong di tengah karakter UTF-8
    while j < #kode and kode:byte(j + 1) >= 0x80 and kode:byte(j + 1) < 0xC0 do j = j + 1 end
    runs[#runs + 1] = '<w:r><w:instrText xml:space="preserve">' .. esc(kode:sub(i, j)) .. '</w:instrText></w:r>'
    i = j + 1
  end
  runs[#runs + 1] = '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
  return pandoc.RawInline("openxml", table.concat(runs))
end

local function akhir_bidang()
  return pandoc.RawInline("openxml", '<w:r><w:fldChar w:fldCharType="end"/></w:r>')
end

---------------------------------------------------------------- RTF
-- formattedCitation: RTF seperti keluaran citeproc-js Zotero untuk Word.
local function rtf_teks(s)
  local out = {}
  for _, c in utf8.codes(s) do
    if c == 92 or c == 123 or c == 125 then out[#out + 1] = "\\" .. utf8.char(c)
    elseif c < 128 then out[#out + 1] = utf8.char(c)
    else
      if c > 0xFFFF then -- pasangan surrogate
        c = c - 0x10000
        local hi, lo = 0xD800 + (c >> 10), 0xDC00 + (c & 0x3FF)
        out[#out + 1] = "\\uc0\\u" .. (hi - 65536) .. "{}\\uc0\\u" .. (lo - 65536) .. "{}"
      else
        if c > 32767 then c = c - 65536 end
        out[#out + 1] = "\\uc0\\u" .. c .. "{}"
      end
    end
  end
  return table.concat(out)
end

local function rtf(inls)
  local out, kaya = {}, false
  local function bungkus(kode, isi) kaya = true; return "{\\" .. kode .. " " .. rtf(isi) .. "}" end
  for _, el in ipairs(inls) do
    local t = el.t
    if t == "Str" then out[#out + 1] = rtf_teks(el.text)
    elseif t == "Space" or t == "SoftBreak" then out[#out + 1] = " "
    elseif t == "Emph" then out[#out + 1] = bungkus("i", el.content)
    elseif t == "Strong" then out[#out + 1] = bungkus("b", el.content)
    elseif t == "SmallCaps" then out[#out + 1] = bungkus("scaps", el.content)
    elseif t == "Superscript" then out[#out + 1] = bungkus("super", el.content)
    elseif t == "Subscript" then out[#out + 1] = bungkus("sub", el.content)
    elseif t == "Quoted" then
      local a, b = "\u{201C}", "\u{201D}"
      if el.quotetype == "SingleQuote" then a, b = "\u{2018}", "\u{2019}" end
      out[#out + 1] = rtf_teks(a) .. rtf(el.content) .. rtf_teks(b)
    elseif el.content and type(el.content) ~= "string" then out[#out + 1] = rtf(el.content)
    elseif t == "Code" or t == "Math" then out[#out + 1] = rtf_teks(el.text)
    end
  end
  return table.concat(out), kaya
end

local function rtf_sitasi(inls)
  local s = rtf(inls)
  if s:find("\\", 1, true) or s:find("{", 1, true) then return "{\\rtf " .. s .. "}" end
  return s
end

---------------------------------------------------------------- locator
-- Sufiks Pandoc ", hlm. 770" -> locator "770", label "page".
local LABEL = {
  p = "page", pp = "page", page = "page", pages = "page", hlm = "page", h = "page",
  hal = "page", halaman = "page",
  bab = "chapter", chap = "chapter", chapter = "chapter", ch = "chapter",
  bag = "section", bagian = "section", sec = "section", section = "section",
  ["§"] = "section", ["§§"] = "section",
  gambar = "figure", gbr = "figure", fig = "figure", figure = "figure",
  vol = "volume", jil = "volume", jilid = "volume", volume = "volume",
  n = "note", catatan = "note", note = "note",
  para = "paragraph", paragraf = "paragraph", par = "paragraph",
  bk = "book", buku = "book", book = "book",
  ln = "line", baris = "line", line = "line",
}

local function token_locator(tok)
  return tok:match("^[%dIVXLCivxlc][%w%-\u{2013}\u{2014}]*$") and
    (tok:match("%d") or tok:match("^[IVXLCivxlc]+$"))
end

local function urai_sufiks(s)
  s = s:gsub("^%s+", ""):gsub("%s+$", "")
  local s2 = s:gsub("^,%s*", "")
  local label, sisa = nil, s2
  local kata, lanjut = s2:match("^([^%s%d]+)%s+(.*)$")
  if kata then
    local k = kata:lower():gsub("%.$", "")
    if LABEL[k] then label, sisa = LABEL[k], lanjut end
  end
  if not label and not s2:match("^%d") then return nil, nil, s end
  -- token pertama locator, lalu ", token" selama berupa nomor
  local tok, rest = sisa:match("^([^%s,;]+)(.*)$")
  if not tok or not token_locator(tok) then return nil, nil, s end
  local loc = tok
  while true do
    local sep, t2, r2 = rest:match("^(,%s*)([^%s,;]+)(.*)$")
    if t2 and token_locator(t2) then loc = loc .. sep .. t2; rest = r2 else break end
  end
  return loc, label or "page", rest
end

---------------------------------------------------------------- data butir
local function data_csl(doc)
  local ok, refs = pcall(pandoc.utils.references, doc)
  if not ok then
    io.stderr:write("[zotero-word] gagal membaca pustaka: " .. tostring(refs) .. "\n")
    return {}
  end
  local d = pandoc.Pandoc({}, pandoc.Meta({references = refs}))
  local arr = pandoc.json.decode(pandoc.write(d, "csljson"), false)
  local peta = {}
  for _, it in ipairs(arr) do
    -- @misc menjadi type "" di Pandoc; Zotero memerlukan jenis CSL yang sah
    if not it.type or it.type == "" then it.type = "document" end
    peta[it.id] = it
  end
  return peta
end

local function kunci_uri(id)
  return URI_DASAR .. id:gsub("[^%w]", "_")
end

---------------------------------------------------------------- sitasi
local PETA, KE = {}, 0

local function butir_sitasi(c)
  local it = PETA[c.id]
  if not it then return nil end
  local b = {id = c.id, uris = {kunci_uri(c.id)}, itemData = it}
  local pre = pandoc.utils.stringify(c.prefix or {})
  if pre ~= "" then b.prefix = pre end
  local suf = pandoc.utils.stringify(c.suffix or {})
  if suf ~= "" then
    local loc, label, sisa = urai_sufiks(suf)
    if loc then b.locator = loc; b.label = label end
    -- sisa sesudah locator dipertahankan apa adanya (", catatan kaki")
    if sisa and sisa:match("%S") then b.suffix = sisa end
  end
  if c.mode == "SuppressAuthor" then b["suppress-author"] = true end
  return b
end

-- inlines -> teks polos seperti Word membaca hasil bidang
local function polos(inls)
  return pandoc.utils.stringify(pandoc.Inlines(inls):walk({
    Space = function() return pandoc.Str(" ") end,
    SoftBreak = function() return pandoc.Str(" ") end,
    LineBreak = function() return pandoc.Str("\n") end,
  }))
end

local function bidang_sitasi(citations, hasil, naratif)
  local items = {}
  for _, c in ipairs(citations) do
    local b = butir_sitasi(c)
    if not b then return nil end
    if naratif then b["suppress-author"] = true end
    items[#items + 1] = b
  end
  KE = KE + 1
  local kunci = {}
  for _, c in ipairs(citations) do kunci[#kunci + 1] = c.id end
  local json = pandoc.json.encode({
    citationID = id_acak(KE .. ":" .. table.concat(kunci, ";")),
    properties = {
      formattedCitation = rtf_sitasi(hasil),
      plainCitation = polos(hasil),
      noteIndex = 0,
    },
    citationItems = items,
    schema = SKEMA,
  })
  jumlah.sitasi = jumlah.sitasi + 1
  jumlah.butir = jumlah.butir + #items
  local out = pandoc.Inlines({awal_bidang("ADDIN ZOTERO_ITEM CSL_CITATION " .. json)})
  out:extend(hasil)
  out:insert(akhir_bidang())
  return out
end

-- Pandoc "@a; @b" naratif -> dipecah per sitasi sebelum citeproc
local function pecah_naratif(inls)
  local out, ubah = pandoc.Inlines({}), false
  for _, el in ipairs(inls) do
    if el.t == "Cite" and #el.citations > 1 and el.citations[1].mode == "AuthorInText" then
      ubah = true
      for i, c in ipairs(el.citations) do
        if i > 1 then out:insert(pandoc.Str(";")); out:insert(pandoc.Space()) end
        out:insert(pandoc.Cite({pandoc.Str("@" .. c.id)}, {c}))
      end
    else
      out:insert(el)
    end
  end
  return ubah and out or nil
end

local function Cite(el)
  local cs = el.citations
  for _, c in ipairs(cs) do
    if not PETA[c.id] then jumlah.tanpa_data = jumlah.tanpa_data + 1; return nil end
  end
  local isi = el.content
  if #cs == 1 and cs[1].mode == "AuthorInText" then
    -- "Mroz (1987, hlm. 770)": nama penulis teks biasa, sisanya bidang
    for i, x in ipairs(isi) do
      if x.t == "Str" and x.text:sub(1, 1) == "(" then
        local nama, sisa = pandoc.Inlines({}), pandoc.Inlines({})
        for k = 1, i - 1 do nama:insert(isi[k]) end
        for k = i, #isi do sisa:insert(isi[k]) end
        local f = bidang_sitasi(cs, sisa, true)
        if not f then return nil end
        jumlah.naratif = jumlah.naratif + 1
        nama:extend(f)
        return nama
      end
    end
  end
  return bidang_sitasi(cs, isi, false)
end

---------------------------------------------------------------- daftar pustaka
local function bibl(div)
  -- cari Para/Plain pertama dan terakhir di dalam entri
  local total = 0
  div:walk({Para = function() total = total + 1 end, Plain = function() total = total + 1 end})
  if total == 0 then return nil end
  local paras = {n = total}
  local n = 0
  local function tandai(blk)
    n = n + 1
    if n == 1 then
      blk.content:insert(1, awal_bidang('ADDIN ZOTERO_BIBL {"uncited":[],"omitted":[],"custom":[]} CSL_BIBLIOGRAPHY'))
    end
    if n == paras.n then blk.content:insert(akhir_bidang()) end
    return blk
  end
  jumlah.bibl = jumlah.bibl + 1
  return div:walk({Para = tandai, Plain = tandai})
end

---------------------------------------------------------------- preferensi
local function id_gaya(meta)
  if meta["zotero-word-style"] then return pandoc.utils.stringify(meta["zotero-word-style"]) end
  local csl = meta.csl and pandoc.utils.stringify(meta.csl)
  if csl then
    local f = io.open(csl, "r")
    if f then
      local t = f:read("a"); f:close()
      local info = t:match("<info>(.-)</info>") or t
      local id = info:match("<id>%s*(.-)%s*</id>")
      if id then return id end
    end
  end
  return "http://www.zotero.org/styles/chicago-author-date"
end

local function preferensi(meta)
  local gaya = id_gaya(meta)
  local bahasa = meta.lang and pandoc.utils.stringify(meta.lang) or nil
  local judul = meta.title and pandoc.utils.stringify(meta.title) or "dokumen"
  local data = '<data data-version="3" zotero-version="7.0">' ..
    '<session id="' .. id_acak("sesi:" .. judul) .. '"/>' ..
    '<style id="' .. esc(gaya):gsub('"', "&quot;") .. '" ' ..
    (bahasa and ('locale="' .. esc(bahasa) .. '" ') or '') ..
    'hasBibliography="1" bibliographyStyleHasBeenSet="1"/>' ..
    '<prefs><pref name="fieldType" value="Field"/>' ..
    '<pref name="automaticJournalAbbreviations" value="false"/></prefs></data>'
  local i, n = 1, 0
  while i <= #data do
    n = n + 1
    meta["ZOTERO_PREF_" .. n] = pandoc.MetaString(data:sub(i, i + 254))
    i = i + 255
  end
  return gaya, n
end

function Pandoc(doc)
  local nyala = doc.meta["zotero-word"]
  if nyala == false or (nyala and pandoc.utils.stringify(nyala) == "false") then return nil end
  if not pandoc.utils.citeproc then
    io.stderr:write("[zotero-word] Pandoc terlalu lama (perlu pandoc.utils.citeproc); dilewati\n")
    return nil
  end
  local ada = false
  doc:walk({Cite = function() ada = true end})
  if not ada then return nil end

  -- sitasi naratif ganda dipecah agar setiap sitasi bisa bersuppress-author
  doc = doc:walk({Inlines = pecah_naratif})
  PETA = data_csl(doc)
  doc = pandoc.utils.citeproc(doc)
  doc = doc:walk({Cite = Cite})
  doc = doc:walk({Div = function(d) if d.identifier == "refs" then return bibl(d) end end})

  doc.meta["suppress-bibliography"] = true
  local gaya, n_pref = preferensi(doc.meta)
  io.stderr:write(string.format(
    "[zotero-word] ZOTERO_ITEM %d (butir %d, naratif %d), ZOTERO_BIBL %d, tanpa data %d, " ..
    "gaya %s, ZOTERO_PREF %d\n",
    jumlah.sitasi, jumlah.butir, jumlah.naratif, jumlah.bibl, jumlah.tanpa_data, gaya, n_pref))
  return doc
end
