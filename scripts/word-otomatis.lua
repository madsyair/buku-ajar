-- Fitur otomatis Word untuk keluaran DOCX buku ajar (skill buku-ajar).
-- Hanya aktif bila FORMAT == "docx"; untuk PDF filter ini tidak berbuat apa-apa.
-- Dipasang di _quarto.yml sebagai filter "at: post-render", yaitu sesudah
-- Quarto menomori bab, gambar, tabel, dan persamaan serta mengganti @fig-,
-- @tbl-, @eq-, dan @sec- menjadi teks; filter ini lalu mengganti nomor statis
-- itu dengan bidang (field) Word yang dapat diperbarui dengan F9:
--
--   * judul bab:      {SEQ Bab} (lampiran: {SEQ Lampiran \* ALPHABETIC});
--     subbab:         {SEQ Bab \c}.{SEQ Subbab \s 1}, dan seterusnya;
--   * keterangan:     Gambar {SEQ Bab \c}.{SEQ Gambar \s 1} (sama untuk Tabel);
--   * persamaan:      ({SEQ Bab \c}.{SEQ Persamaan \s 1}) di tabel tanpa garis,
--                     rumus di tengah dan nomor di kanan;
--   * rujukan silang: {REF _Ref_<label> \h}; setiap nomor di atas dibungkus
--                     bookmark _Ref_<label>;
--   * sesudah halaman hak cipta (Div custom-style "Hak Cipta"): Daftar Isi
--     {TOC \o "1-2"}, Daftar Gambar {TOC \h \z \c "Gambar"}, dan Daftar Tabel
--     {TOC \h \z \c "Tabel"};
--   * judul lampiran "Appendix" -> "Lampiran"; teks alternatif gambar; lebar
--     gambar <= bidang teks - 0,5 cm; lebar minimum kolom tabel; kode sebaris
--     0,8 x ukuran teks.
--
-- Bidang teks dan ukuran teks dibaca dari reference-doc (w:pgSz, w:pgMar,
-- gaya Body Text), sehingga filter ini mengikuti ukuran buku dan profil
-- penerbit dari huruf.py tanpa disunting. Metadata opsional (mis. di format
-- docx _quarto.yml) menimpanya: word-bidang-teks-cm: 12.
--
-- Penomoran per bab memakai SEQ Bab \c, bukan STYLEREF 1 \s, karena nomor bab
-- dari Quarto adalah teks biasa (bukan penomoran daftar Word); STYLEREF \s
-- hanya membaca nomor daftar. Hasil awal setiap bidang diisi sama persis
-- dengan nomor di PDF, sehingga dokumen benar walaupun bidang belum diperbarui.
-- Rincian dan batasan: references/aturan-gaya-dan-tampilan.md, "Rumus dan
-- fitur otomatis di Word".

if not FORMAT:match("docx") then return {} end

local ID = 900000          -- id bookmark; jauh di atas id buatan Pandoc
local bookmark = {}        -- label -> nama bookmark
local jumlah = {gambar = 0, tabel = 0, persamaan = 0, ref = 0}
-- entri awal daftar isi/gambar/tabel (hasil bidang sebelum diperbarui Word)
local entri = {isi = {}, Gambar = {}, Tabel = {}}

-- Bidang teks (cm) dan ukuran teks (setengah poin) dari reference-doc;
-- bawaan B5 seri: 12 cm, 10,5 pt (21).
local BIDANG_CM, SZ_TEKS = 12.0, 21
do
  local ok = pcall(function()
    local ref = PANDOC_WRITER_OPTIONS and PANDOC_WRITER_OPTIONS.reference_doc
    if not ref or not pandoc.zip then return end
    local f = io.open(ref, "rb")
    if not f then return end
    local data = f:read("a"); f:close()
    local arsip = pandoc.zip.Archive(data)
    for _, e in ipairs(arsip.entries) do
      if e.path == "word/document.xml" then
        local x = e:contents()
        local w = tonumber(x:match('<w:pgSz[^>]-w:w="(%d+)"'))
        local mar = x:match('<w:pgMar [^>]*>') or ""
        local l, r = tonumber(mar:match('w:left="(%d+)"')), tonumber(mar:match('w:right="(%d+)"'))
        if w and l and r and w > l + r then BIDANG_CM = (w - l - r) * 2.54 / 1440 end
      elseif e.path == "word/styles.xml" then
        local st = e:contents():match('<w:style [^>]-w:styleId="BodyText".-</w:style>')
        local sz = st and tonumber(st:match('<w:sz w:val="(%d+)"'))
        if sz then SZ_TEKS = sz end
      end
    end
  end)
end
local LEBAR_GAMBAR_CM = BIDANG_CM - 0.5   -- sel tabel Quarto lebih sempit dari bidang teks

local function esc(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

local function nama_bm(label)
  if bookmark[label] then return bookmark[label] end
  local n = "_Ref_" .. label:gsub("[^%w]", "_")
  if #n > 40 then
    local h = 0
    for i = 1, #label do h = (h * 31 + label:byte(i)) % 1000000 end
    n = n:sub(1, 33) .. string.format("%06d", h)
  end
  bookmark[label] = n
  return n
end

local function field(instr, hasil)
  return '<w:r><w:fldChar w:fldCharType="begin"/></w:r>' ..
    '<w:r><w:instrText xml:space="preserve"> ' .. esc(instr) .. ' </w:instrText></w:r>' ..
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r>' ..
    '<w:r><w:t xml:space="preserve">' .. esc(hasil) .. '</w:t></w:r>' ..
    '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
end

local function teks_run(s)
  return '<w:r><w:t xml:space="preserve">' .. esc(s) .. '</w:t></w:r>'
end

local function dengan_bookmark(label, isi)
  ID = ID + 1
  return '<w:bookmarkStart w:id="' .. ID .. '" w:name="' .. nama_bm(label) .. '"/>' ..
    isi .. '<w:bookmarkEnd w:id="' .. ID .. '"/>'
end

-- Nomor bab angka -> SEQ Bab; huruf (lampiran) -> SEQ Lampiran.
local function seq_bab_c(nomor_bab)
  if not nomor_bab:match("^%d+$") then
    return field("SEQ Lampiran \\c \\* ALPHABETIC", nomor_bab)
  end
  return field("SEQ Bab \\c \\* ARABIC", nomor_bab)
end

-- "2.3" -> bidang {SEQ Bab \c}.{SEQ <nama> \s 1}. Nomor pertama di setiap
-- bab juga diberi \r 1: Word sudah mengulang dari 1 lewat \s 1, tetapi
-- LibreOffice mengabaikan \s sehingga perlu \r agar nomornya tetap benar.
local function seq_anak(nama, ke, sakelar)
  local r = (ke == "1") and " \\r 1" or ""
  return field("SEQ " .. nama .. " \\* ARABIC" .. r .. " " .. sakelar, ke)
end

local function nomor_berbidang(nomor, nama)
  -- bab tanpa nomor (Prakata): "Tabel 1"
  if nomor:match("^%d+$") then return seq_anak(nama, nomor, "\\s 1") end
  local bab, ke = nomor:match("^([%dA-Z]+)%.(%d+)$")
  if not bab then return nil end
  return seq_bab_c(bab) .. teks_run(".") .. seq_anak(nama, ke, "\\s 1")
end

-- Teks polos untuk entri daftar: rumus sebaris diubah kira-kira ke Unicode
-- ("\\hat k" -> "k̂", "\\alpha" -> "α") agar TeX mentah tidak tampil.
local YUNANI = {alpha="α", beta="β", gamma="γ", delta="δ", epsilon="ε", varepsilon="ε",
  zeta="ζ", eta="η", theta="θ", kappa="κ", lambda="λ", mu="μ", nu="ν", xi="ξ", pi="π",
  rho="ρ", sigma="σ", tau="τ", phi="φ", varphi="φ", chi="χ", psi="ψ", omega="ω",
  Gamma="Γ", Delta="Δ", Theta="Θ", Lambda="Λ", Sigma="Σ", Phi="Φ", Psi="Ψ", Omega="Ω",
  mid="∣", sim="∼", times="×", le="≤", ge="≥", ne="≠", approx="≈", cdot="·", infty="∞"}
local AKSEN = {hat = "\u{302}", bar = "\u{304}", tilde = "\u{303}"}
local function tex_polos(t)
  t = t:gsub("\\(%a+)", function(c) return YUNANI[c] end)
  t = t:gsub("\\(%a+)%s*{([^{}]*)}", function(c, x)
    if AKSEN[c] then return x .. AKSEN[c] end
    return x
  end)
  t = t:gsub("\\(%a+)%s+([%w\128-\255][\128-\191]*)", function(c, x)
    return AKSEN[c] and (x .. AKSEN[c]) end)
  t = t:gsub("\\%a+", ""):gsub("\\.", " "):gsub("[{}]", ""):gsub("%s+", " ")
  return t
end
local function teks_polos(x)
  local isi = pandoc.Inlines(x):walk({Math = function(m) return pandoc.Str(tex_polos(m.text)) end})
  return pandoc.utils.stringify(isi)
end

---------------------------------------------------------------- judul bab
local function Header(h)
  local nomor = h.attributes["number"]
  local c = h.content
  -- Lampiran: "Appendix A — Judul" -> "Lampiran A — Judul"
  if h.level == 1 and c[1] and c[1].t == "Str" and c[1].text == "Appendix" then
    c[1] = pandoc.Str("Lampiran")
  end
  if h.level <= 2 and h.identifier ~= "" then
    table.insert(entri.isi, {h.level, teks_polos(c), h.identifier})
  end
  if not nomor then return h end
  local isi
  if h.level == 1 then
    if nomor:match("^%d+$") then
      isi = field("SEQ Bab \\* ARABIC", nomor)
    elseif nomor:match("^[A-Z]$") then
      isi = field("SEQ Lampiran \\* ALPHABETIC", nomor)
    end
  elseif h.level == 2 then
    local bab, ke = nomor:match("^([%dA-Z]+)%.(%d+)$")
    if bab then
      isi = seq_bab_c(bab) .. teks_run(".") .. seq_anak("Subbab", ke, "\\s 1")
    end
  elseif h.level == 3 then
    local bab, sb, ke = nomor:match("^([%dA-Z]+)%.(%d+)%.(%d+)$")
    if bab then
      isi = seq_bab_c(bab) .. teks_run(".") .. field("SEQ Subbab \\c \\* ARABIC", sb) ..
        teks_run(".") .. seq_anak("Subsubbab", ke, "\\s 2")
    end
  end
  if not isi then return h end
  -- cari Str yang sama dengan nomor (Quarto menaruhnya di awal judul)
  for i, el in ipairs(c) do
    if el.t == "Str" and el.text == nomor then
      if h.identifier ~= "" then isi = dengan_bookmark(h.identifier, isi) end
      c[i] = pandoc.RawInline("openxml", isi)
      break
    end
  end
  return h
end

---------------------------------------------------------------- keterangan
-- Paragraf keterangan Quarto: RawInline(pPr ImageCaption), Str "Gambar",
-- Str "\u{a0}", Str "2.3", Str ":", ...
local function keterangan(para, label)
  local c = para.content
  for i = 1, math.min(#c, 4) do
    local el = c[i]
    if el.t == "Str" and (el.text == "Gambar" or el.text == "Tabel") then
      local j = i + 1
      if c[j] and c[j].t == "Str" and c[j].text == "\u{a0}" then j = j + 1 end
      local no = c[j]
      if no and no.t == "Str" then
        local nama = el.text
        local isi = nomor_berbidang(no.text, nama)
        if isi then
          local t = teks_polos(para.content):gsub("^%s+", "")
          table.insert(entri[nama], {1, t, label})
          c[j] = pandoc.RawInline("openxml", dengan_bookmark(label, isi))
          if nama == "Gambar" then jumlah.gambar = jumlah.gambar + 1
          else jumlah.tabel = jumlah.tabel + 1 end
          return true
        end
      end
    end
  end
  return false
end

local function teks_keterangan(para)
  local s = teks_polos(para.content)
  return (s:gsub("^%s*Gambar.-:%s*", ""))
end

local function Div(d)
  local label = d.identifier
  if not (label:match("^fig%-") or label:match("^tbl%-")) then return nil end
  local judul
  -- keterangan langsung di dalam Div (bukan subgambar)
  for _, b in ipairs(d.content) do
    if b.t == "Para" and keterangan(b, label) then judul = teks_keterangan(b); break end
  end
  -- teks alternatif gambar: fig-alt bila ada, selain itu judul gambar
  if label:match("^fig%-") then
    d = d:walk({Image = function(img)
      -- Lebar maksimum = bidang teks - 0,5 cm: gambar berada di sel tabel
      -- Quarto yang lebih sempit sekitar 0,4 cm dari bidang teks; Pandoc hanya
      -- menyesuaikan ke bidang teks sehingga tepi kanan gambar terpotong.
      if not img.attributes["width"] then
        local ok, _, isi = pcall(pandoc.mediabag.fetch, img.src)
        -- pandoc.image ada sejak Pandoc 3.1.10 (Quarto 1.5+ membawanya)
        if ok and isi and pandoc.image then
          local ok2, uk = pcall(pandoc.image.size, isi)
          if ok2 and uk and uk.width and uk.dpi_horz and uk.dpi_horz > 0 then
            if uk.width / uk.dpi_horz * 2.54 > LEBAR_GAMBAR_CM then
              img.attributes["width"] = string.format("%.1fcm", LEBAR_GAMBAR_CM)
            end
          end
        end
      end
      if #img.caption == 0 then
        local alt = img.attributes["fig-alt"] or img.attributes["alt"] or judul
        if alt and alt ~= "" then img.caption = {pandoc.Str(alt)} end
      end
      return img
    end})
  end
  return d
end

---------------------------------------------------------------- persamaan
-- Para berisi Span(eq-...)[Math DisplayMath "... \qquad(2.1)"] dipecah:
-- teks sebelum, tabel 1x2 tanpa garis (rumus | nomor), teks sesudah.
local function tabel_persamaan(label, tex, nomor)
  local isi = nomor_berbidang(nomor, "Persamaan")
  local sel_no = pandoc.Para({pandoc.RawInline("openxml",
    teks_run("(") .. dengan_bookmark(label, isi) .. teks_run(")"))})
  local function sel(blok)
    return pandoc.Cell(blok)
  end
  local baris = pandoc.Row({
    sel({pandoc.Para({pandoc.Math("DisplayMath", tex)})}),
    sel({pandoc.Div({sel_no}, {["custom-style"] = "Nomor Persamaan"})})})
  local tb = pandoc.Table(
    {long = {}},
    {{pandoc.AlignCenter, 0.88}, {pandoc.AlignRight, 0.12}},
    pandoc.TableHead({}),
    {{attr = pandoc.Attr(), body = {baris}, head = {}, row_head_columns = 0}},
    pandoc.TableFoot({}))
  jumlah.persamaan = jumlah.persamaan + 1
  return tb
end

local function pecah_persamaan(blok)
  if blok.t ~= "Para" and blok.t ~= "Plain" then return nil end
  local Wadah = blok.t == "Para" and pandoc.Para or pandoc.Plain
  local ada = false
  for _, el in ipairs(blok.content) do
    if el.t == "Span" and el.identifier:match("^eq%-") then ada = true end
  end
  if not ada then return nil end
  local hasil, sekarang = {}, pandoc.Inlines({})
  local function tutup()
    -- buang spasi di tepi
    while #sekarang > 0 and (sekarang[1].t == "Space" or sekarang[1].t == "SoftBreak") do sekarang:remove(1) end
    while #sekarang > 0 and (sekarang[#sekarang].t == "Space" or sekarang[#sekarang].t == "SoftBreak") do sekarang:remove() end
    if #sekarang > 0 then table.insert(hasil, Wadah(sekarang)) end
    sekarang = pandoc.Inlines({})
  end
  for _, el in ipairs(blok.content) do
    local m = el.t == "Span" and el.identifier:match("^eq%-") and #el.content == 1 and el.content[1]
    if m and m.t == "Math" and m.mathtype == "DisplayMath" then
      local tex, no = m.text:match("^(.-)%s*\\qquad%s*%(([%dA-Z]+%.%d+)%)%s*$")
      if tex then
        tutup()
        table.insert(hasil, tabel_persamaan(el.identifier, tex, no))
      else
        sekarang:insert(el)
      end
    else
      sekarang:insert(el)
    end
  end
  tutup()
  return hasil
end

---------------------------------------------------------------- rujukan
local function Link(l)
  if not l.classes:includes("quarto-xref") then return nil end
  local label = l.target:match("^#(.+)$")
  if not label or not bookmark[label] then return nil end
  local c = l.content
  local akhir = c[#c]
  if not (akhir and akhir.t == "Str") then return nil end
  local nomor = akhir.text
  local out = pandoc.Inlines({})
  for i = 1, #c - 1 do out:insert(c[i]) end
  local ref = field("REF " .. bookmark[label] .. " \\h", nomor)
  if label:match("^eq%-") then
    ref = teks_run("(") .. ref .. teks_run(")")
  end
  out:insert(pandoc.RawInline("openxml", ref))
  jumlah.ref = jumlah.ref + 1
  return out
end

---------------------------------------------------------------- lebar kolom
-- Tabel kable/pipa memberi lebar kolom sebanding panjang isi terpanjang,
-- sehingga kolom berisi kata pendek ("Respons", "Bab") bisa lebih sempit
-- daripada satu kata dan kata itu terpenggal per huruf di Word. Setiap kolom
-- diberi lebar minimum selebar kata terpanjangnya (kira-kira 72 karakter
-- per 12 cm pada teks 10,5 pt); kelebihannya diambil dari kolom lain secara
-- sebanding.
local KARAKTER_PER_BARIS = 72 * (BIDANG_CM / 12) * (21 / SZ_TEKS)
local function kata_terpanjang(blok)
  local m = 0
  for w in pandoc.utils.stringify(blok):gmatch("%S+") do
    local n = utf8.len(w) or #w
    if n > m then m = n end
  end
  return m
end

local function Table(t)
  local cs = t.colspecs
  -- Pembungkus tabel bernomor dari Quarto (satu kolom, rata tengah): rata
  -- tengahnya diwariskan Pandoc ke setiap sel tabel di dalamnya sebagai
  -- <w:jc> kedua, sehingga kolom rata kiri/kanan tampil rata tengah.
  if #cs == 1 then
    local bungkus = false
    for _, b in ipairs(t.bodies) do for _, r in ipairs(b.body) do for _, c in ipairs(r.cells) do
      for _, x in ipairs(c.contents) do
        if x.t == "Div" and x.identifier:match("^tbl%-") then bungkus = true end
      end
    end end end
    if bungkus and cs[1][1] == pandoc.AlignCenter then
      cs[1] = {pandoc.AlignDefault, cs[1][2]}
      t.colspecs = cs
      return t
    end
    return nil
  end
  local w = {}
  for i, c in ipairs(cs) do
    if type(c[2]) ~= "number" then return nil end
    w[i] = c[2]
  end
  local minimum = {}
  local function catat_baris(row)
    for i, cell in ipairs(row.cells) do
      if i <= #cs then
        local m = (kata_terpanjang(cell.contents) + 2) / KARAKTER_PER_BARIS
        minimum[i] = math.max(minimum[i] or 0, m)
      end
    end
  end
  for _, r in ipairs(t.head.rows) do catat_baris(r) end
  for _, b in ipairs(t.bodies) do for _, r in ipairs(b.body) do catat_baris(r) end end
  local jml_min, total = 0, 0
  for i = 1, #cs do minimum[i] = minimum[i] or 0; jml_min = jml_min + minimum[i]; total = total + w[i] end
  if jml_min >= total or jml_min == 0 then return nil end
  local ubah = false
  for _ = 1, 10 do
    local kurang, lebih = 0, 0
    for i = 1, #cs do
      if w[i] < minimum[i] then kurang = kurang + minimum[i] - w[i]; w[i] = minimum[i]; ubah = true
      elseif w[i] > minimum[i] then lebih = lebih + w[i] - minimum[i] end
    end
    if kurang <= 1e-9 then break end
    for i = 1, #cs do
      if w[i] > minimum[i] then w[i] = w[i] - kurang * (w[i] - minimum[i]) / lebih end
    end
  end
  if not ubah then return nil end
  for i, c in ipairs(cs) do cs[i] = {c[1], w[i]} end
  t.colspecs = cs
  return t
end

---------------------------------------------------------------- kode sebaris
-- Blok kode dan keluaran memakai gaya Verbatim Char/Source Code dari
-- reference-doc (B5 seri: 7 pt, seperti PDF 7,2 pt, agar baris sampai sekitar
-- 75 karakter muat di bidang teks 12 cm). Kode sebaris di dalam prosa diberi
-- 0,8 x ukuran teks langsung (B5 seri: 8,5 pt dari teks 10,5 pt).
local SZ_SEBARIS = tostring(math.floor(0.8 * SZ_TEKS + 0.5))
local function Code(c)
  return pandoc.RawInline("openxml",
    '<w:r><w:rPr><w:rStyle w:val="VerbatimChar"/><w:sz w:val="' .. SZ_SEBARIS ..
    '"/><w:szCs w:val="' .. SZ_SEBARIS .. '"/></w:rPr>' ..
    '<w:t xml:space="preserve">' .. esc(c.text) .. '</w:t></w:r>')
end

---------------------------------------------------------------- daftar
-- Hasil awal bidang TOC: entri bertaut tanpa nomor halaman, supaya daftar
-- sudah terbaca di LibreOffice/Google Docs; Word mengisi nomor halaman saat
-- bidang diperbarui (F9 atau updateFields ketika dokumen dibuka).
local function daftar(judul, instr, isi_entri, gaya)
  local awal = '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>' ..
    '<w:r><w:instrText xml:space="preserve"> ' .. esc(instr) .. ' </w:instrText></w:r>' ..
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
  local akhir = '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
  local ps = {}
  if #isi_entri == 0 then
    ps[1] = '<w:p>' .. awal .. teks_run("Perbarui bidang (F9) untuk mengisi daftar ini.") .. akhir .. '</w:p>'
  end
  for i, e in ipairs(isi_entri) do
    local st = gaya or ("TOC" .. e[1])
    ps[#ps + 1] = '<w:p><w:pPr><w:pStyle w:val="' .. st .. '"/></w:pPr>' ..
      (i == 1 and awal or '') ..
      '<w:hyperlink w:anchor="' .. esc(e[3]) .. '" w:history="1"><w:r><w:t xml:space="preserve">' ..
      esc(e[2]) .. '</w:t></w:r></w:hyperlink>' ..
      (i == #isi_entri and akhir or '') .. '</w:p>'
  end
  return pandoc.RawBlock("openxml",
    '<w:sdt><w:sdtPr><w:docPartObj><w:docPartGallery w:val="Table of Contents"/>' ..
    '<w:docPartUnique/></w:docPartObj></w:sdtPr><w:sdtContent>' ..
    '<w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr>' .. teks_run(judul) .. '</w:p>' ..
    table.concat(ps) .. '</w:sdtContent></w:sdt>')
end

local function ganti_halaman()
  return pandoc.RawBlock("openxml", '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
end

function Pandoc(doc)
  -- metadata word-bidang-teks-cm menimpa bidang teks dari reference-doc
  local m = doc.meta["word-bidang-teks-cm"]
  local cm = m and tonumber(pandoc.utils.stringify(m))
  if cm and cm > 2 then
    BIDANG_CM = cm
    LEBAR_GAMBAR_CM = cm - 0.5
    KARAKTER_PER_BARIS = 72 * (cm / 12) * (21 / SZ_TEKS)
  end
  -- 1. nomor (judul, keterangan, persamaan) lebih dulu agar bookmark dikenal
  local blok = doc.blocks:walk({Table = Table})
  blok = blok:walk({Header = Header, Div = Div})
  local baru = pandoc.Blocks({})
  local function proses(bs)
    local out = pandoc.Blocks({})
    for _, b in ipairs(bs) do
      local p = pecah_persamaan(b)
      if p then out:extend(p) else out:insert(b) end
    end
    return out
  end
  blok = proses(blok)
  -- persamaan di dalam Div (kotak, catatan) dan sel tabel
  blok = blok:walk({Blocks = function(bs) return proses(bs) end})
  -- 2. rujukan silang
  blok = blok:walk({Link = Link})
  blok = blok:walk({Code = Code})
  -- 3. daftar isi, daftar gambar, daftar tabel sesudah halaman hak cipta
  local daftar_blok = pandoc.Blocks({
    daftar("Daftar Isi", 'TOC \\o "1-2" \\h \\z \\u', entri.isi), ganti_halaman()})
  if jumlah.gambar > 0 then
    daftar_blok:extend({daftar("Daftar Gambar", 'TOC \\h \\z \\c "Gambar"', entri.Gambar, "TableofFigures"), ganti_halaman()})
  end
  if jumlah.tabel > 0 then
    daftar_blok:extend({daftar("Daftar Tabel", 'TOC \\h \\z \\c "Tabel"', entri.Tabel, "TableofFigures"), ganti_halaman()})
  end
  -- Halaman hak cipta (Div custom-style "Hak Cipta", mis. dari index.qmd
  -- dalam ::: {.content-visible when-format="docx"}) dipindah ke awal isi,
  -- sesudah halaman judul dan sebelum daftar isi (urutan sama dengan PDF).
  local function hak_cipta(b)
    return b.t == "Div" and b.attributes["custom-style"] == "Hak Cipta"
  end
  local pos = 1
  for i = 1, math.min(#blok, 3) do
    if hak_cipta(blok[i]) then pos = i + 1 end
  end
  if pos == 1 then
    local hc
    for i, b in ipairs(blok) do
      if hak_cipta(b) then hc = blok:remove(i); break end
      if b.t == "Div" then
        for j, x in ipairs(b.content) do
          if hak_cipta(x) then hc = b.content:remove(j); break end
        end
        if hc then break end
      end
    end
    if hc then
      blok:insert(1, ganti_halaman())
      blok:insert(2, hc)
      pos = 3
    end
  end
  for k = #daftar_blok, 1, -1 do blok:insert(pos, daftar_blok[k]) end
  doc.blocks = blok
  io.stderr:write(string.format(
    "[word-otomatis] bidang teks %.1f cm; SEQ Gambar %d, SEQ Tabel %d, SEQ Persamaan %d, REF %d\n",
    BIDANG_CM, jumlah.gambar, jumlah.tabel, jumlah.persamaan, jumlah.ref))
  return doc
end
