import os
import sys
import re
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

sys.stdout.reconfigure(encoding="utf-8")

OUT_DIR = r"c:\Users\Nor Anisa\Downloads\LOMBA SI\B-OUTDOOR"
IMG_DIR = os.path.join(OUT_DIR, "img")

TITLE_TEXT = (
    "B-OUTDOOR: RANCANG BANGUN GEOPORTAL WISATA PETUALANGAN PERBUKITAN "
    "KALIMANTAN SELATAN DAN KONSERVASI SUNGAI BERBASIS KOMUNITAS PECINTA ALAM "
    "DI KOTA BANJARMASIN"
)

MATH_NS = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

def m_r(text, italic=True, bold=False):
    it_xml = "" if italic else '<m:sty m:val="p"/>'
    b_xml = "<w:b/>" if bold else ""
    i_xml = "<w:i/>" if italic else "<w:i w:val=\"0\"/>"
    return (
        f'<m:r>'
        f'<m:rPr>{it_xml}</m:rPr>'
        f'<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math" w:cs="Cambria Math"/><w:sz w:val="24"/><w:szCs w:val="24"/>{b_xml}{i_xml}</w:rPr>'
        f'<m:t>{text}</m:t>'
        f'</m:r>'
    )

def m_sub(base_xml, sub_xml):
    return f'<m:sSub><m:e>{base_xml}</m:e><m:sub>{sub_xml}</m:sub></m:sSub>'

def m_sup(base_xml, sup_xml):
    return f'<m:sSup><m:e>{base_xml}</m:e><m:sup>{sup_xml}</m:sup></m:sSup>'

def m_frac(num_xml, den_xml):
    return f'<m:f><m:num>{num_xml}</m:num><m:den>{den_xml}</m:den></m:f>'

def m_rad(deg_xml, base_xml):
    if deg_xml:
        return f'<m:rad><m:deg>{deg_xml}</m:deg><m:e>{base_xml}</m:e></m:rad>'
    return f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>{base_xml}</m:e></m:rad>'

def m_nary(chr_val, sub_xml, sup_xml, e_xml):
    return (
        f'<m:nary>'
        f'<m:naryPr><m:chr m:val="{chr_val}"/><m:limLoc m:val="undOvr"/></m:naryPr>'
        f'<m:sub>{sub_xml}</m:sub>'
        f'<m:sup>{sup_xml}</m:sup>'
        f'<m:e>{e_xml}</m:e>'
        f'</m:nary>'
    )

def m_delim(beg_chr, end_chr, base_xml):
    return f'<m:d><m:dPr><m:begChr m:val="{beg_chr}"/><m:endChr m:val="{end_chr}"/></m:dPr><m:e>{base_xml}</m:e></m:d>'

def add_omml_equation(doc, omath_inner_xml, eq_num):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    tblPr = tbl._tbl.tblPr
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>')
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblW)
    tblPr.append(tblBorders)

    c_eq = tbl.rows[0].cells[0]
    c_num = tbl.rows[0].cells[1]

    c_eq.width = Cm(12.4)
    c_num.width = Cm(1.6)

    c_eq._tc.get_or_add_tcPr().append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="4428" w:type="pct"/>'))
    c_num._tc.get_or_add_tcPr().append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="572" w:type="pct"/>'))

    for cell in (c_eq, c_num):
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'</w:tcBorders>'
        ))

    p_eq = c_eq.paragraphs[0]
    p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eq.paragraph_format.space_before = Pt(3)
    p_eq.paragraph_format.space_after = Pt(3)
    p_eq.paragraph_format.line_spacing = 1.15
    p_eq.paragraph_format.first_line_indent = Cm(0)

    omath_el = parse_xml(f'<m:oMath {MATH_NS}>{omath_inner_xml}</m:oMath>')
    p_eq._p.append(omath_el)

    p_num = c_num.paragraphs[0]
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_num.paragraph_format.space_before = Pt(3)
    p_num.paragraph_format.space_after = Pt(3)
    p_num.paragraph_format.line_spacing = 1.15
    p_num.paragraph_format.first_line_indent = Cm(0)
    r_num = p_num.add_run(f"({eq_num})")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    r_num.font.bold = False

def configure_section_margins(sec):
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(4.0)
    sec.right_margin = Cm(3.0)
    sec.top_margin = Cm(4.0)
    sec.bottom_margin = Cm(3.0)
    sec.header_distance = Cm(1.5)
    sec.footer_distance = Cm(1.5)

def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    r = run._r
    r.append(fldChar1)
    r.append(instrText)
    r.append(fldChar2)
    r.append(fldChar3)

def set_Normal_style(doc):
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    pf = style.paragraph_format
    pf.left_indent = Cm(0)
    pf.right_indent = Cm(0)
    pf.space_before = Pt(0)
    pf.space_after = Pt(4)
    pf.line_spacing = 1.5

def add_center_bold(doc, text, size=12, space_before=0, space_after=4, line_spacing=1.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.left_indent = Cm(0)
    p.paragraph_format.right_indent = Cm(0)
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    r.font.bold = True
    return p

def add_bab_header(doc, bab_num, bab_title, page_break=False):
    if page_break:
        doc.add_page_break()
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.first_line_indent = Cm(0)
    p1.paragraph_format.space_before = Pt(10 if not page_break else 0)
    p1.paragraph_format.space_after = Pt(2)
    p1.paragraph_format.line_spacing = 1.5
    p1.paragraph_format.keep_with_next = True
    r1 = p1.add_run(bab_num)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    r1.font.bold = True

    if bab_title:
        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.first_line_indent = Cm(0)
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(8)
        p2.paragraph_format.line_spacing = 1.5
        p2.paragraph_format.keep_with_next = True
        r2 = p2.add_run(bab_title)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(12)
        r2.font.bold = True

def add_sub_bab(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Cm(0)
    p.paragraph_format.right_indent = Cm(0)
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    return p

def add_sub_sub_bab(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Cm(0)
    p.paragraph_format.right_indent = Cm(0)
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.italic = True
    return p

def append_formatted_tokens(p, text):
    tokens = re.split(r'(\{[A-Za-z0-9_]+\})', text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('{') and tok.endswith('}'):
            key = tok[1:-1]
            if key in ('f_i', 'd_i', 's_i', 'WQI_i', 'TDS_i', 'pH_i'):
                base, sub = key.split('_')
                r1 = p.add_run(base)
                r1.font.name = "Times New Roman"; r1.font.size = Pt(12); r1.font.italic = True
                r2 = p.add_run(sub)
                r2.font.name = "Times New Roman"; r2.font.size = Pt(12); r2.font.italic = True; r2.font.subscript = True
            elif key == 'lambda':
                r1 = p.add_run("\u03bb")
                r1.font.name = "Times New Roman"; r1.font.size = Pt(12); r1.font.italic = True
            elif key in ('i', 'r', 'h', 'n', 'k', 'N'):
                r1 = p.add_run(key)
                r1.font.name = "Times New Roman"; r1.font.size = Pt(12); r1.font.italic = True
            else:
                r1 = p.add_run(key)
                r1.font.name = "Times New Roman"; r1.font.size = Pt(12)
        else:
            r = p.add_run(tok)
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)

def add_para(doc, text, indent=True, space_after=4, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.left_indent = Cm(0)
    p.paragraph_format.right_indent = Cm(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.first_line_indent = Cm(1.25) if indent else Cm(0)
    append_formatted_tokens(p, text)
    return p

def add_numbered_item(doc, num, bold_prefix, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.right_indent = Cm(0)
    p.paragraph_format.first_line_indent = Cm(-0.75)
    r_num = p.add_run(f"{num}. ")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Times New Roman"
        rb.font.size = Pt(12)
        rb.font.bold = True
    append_formatted_tokens(p, text)
    return p

def add_styled_table(doc, caption, headers, rows, col_widths_cm):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.left_indent = Cm(0)
    p_cap.paragraph_format.right_indent = Cm(0)
    p_cap.paragraph_format.first_line_indent = Cm(0)
    p_cap.paragraph_format.space_before = Pt(6)
    p_cap.paragraph_format.space_after = Pt(3)
    p_cap.paragraph_format.line_spacing = 1.15
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10.5)
    r_cap.font.bold = True

    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    tblPr = tbl._tbl.tblPr
    tblPr.append(parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>'))
    tblPr.append(parse_xml(
        f'<w:tblCellMar {nsdecls("w")}>'
        f'<w:top w:w="60" w:type="dxa"/>'
        f'<w:left w:w="90" w:type="dxa"/>'
        f'<w:bottom w:w="60" w:type="dxa"/>'
        f'<w:right w:w="90" w:type="dxa"/>'
        f'</w:tblCellMar>'
    ))

    total_w = sum(col_widths_cm)
    pct_widths = [int(round((w / total_w) * 5000)) for w in col_widths_cm]

    for ci, h in enumerate(headers):
        cell = tbl.rows[0].cells[ci]
        cell.width = Cm(col_widths_cm[ci])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{pct_widths[ci]}" w:type="pct"/>'))
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "166534") # Forest Green
        shd.set(qn("w:val"), "clear")
        tcPr.append(shd)

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.left_indent = Cm(0)
        p.paragraph_format.right_indent = Cm(0)
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for ri, row_data in enumerate(rows):
        for ci, val in enumerate(row_data):
            cell = tbl.rows[ri + 1].cells[ci]
            cell.width = Cm(col_widths_cm[ci])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{pct_widths[ci]}" w:type="pct"/>'))
            if ri % 2 == 1:
                shd = OxmlElement("w:shd")
                shd.set(qn("w:fill"), "F0FDF4") # Light Green Shading
                shd.set(qn("w:val"), "clear")
                tcPr.append(shd)

            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if ci > 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.left_indent = Cm(0)
            p.paragraph_format.right_indent = Cm(0)
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)



def add_figure(doc, img_filename, caption, width_cm=13.0):
    img_path = os.path.join(IMG_DIR, img_filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.left_indent = Cm(0)
        p_img.paragraph_format.right_indent = Cm(0)
        p_img.paragraph_format.first_line_indent = Cm(0)
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Cm(min(width_cm, 13.8)))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.left_indent = Cm(0)
    p_cap.paragraph_format.right_indent = Cm(0)
    p_cap.paragraph_format.first_line_indent = Cm(0)
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(6)
    p_cap.paragraph_format.line_spacing = 1.15
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10.5)
    r_cap.font.italic = True

def build_full_paper_b_outdoor():
    doc = docx.Document()
    set_Normal_style(doc)

    sec = doc.sections[0]
    configure_section_margins(sec)
    add_page_number_footer(sec)

    # =========================================================================
    # HALAMAN JUDUL & ABSTRAK (Halaman 1)
    # =========================================================================
    add_center_bold(doc, "KARYA TULIS ILMIAH", size=10.5, space_before=0, space_after=1)
    add_center_bold(doc, "KATEGORI UMUM (MAHASISWA)", size=10.5, space_before=0, space_after=4)

    add_center_bold(doc, TITLE_TEXT, size=11.5, space_before=2, space_after=6, line_spacing=1.15)

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.left_indent = Cm(0)
    p_author.paragraph_format.right_indent = Cm(0)
    p_author.paragraph_format.first_line_indent = Cm(0)
    p_author.paragraph_format.space_before = Pt(0)
    p_author.paragraph_format.space_after = Pt(6)
    p_author.paragraph_format.line_spacing = 1.1
    r_a1 = p_author.add_run("Disusun oleh: ")
    r_a1.font.name = "Times New Roman"; r_a1.font.size = Pt(10.5)
    r_a2 = p_author.add_run("[Nama Mahasiswa Pengusul / Tim Mapala]\n")
    r_a2.font.name = "Times New Roman"; r_a2.font.size = Pt(10.5); r_a2.font.bold = True
    r_a3 = p_author.add_run("Dosen Pembimbing: Nor Anisa, M.Kom.\n")
    r_a3.font.name = "Times New Roman"; r_a3.font.size = Pt(10); r_a3.font.bold = True
    r_a4 = p_author.add_run("Program Studi Sistem Informasi, Universitas Sari Mulia | Surel: noranisa@unism.ac.id")
    r_a4.font.name = "Times New Roman"; r_a4.font.size = Pt(9.5); r_a4.font.italic = True

    add_center_bold(doc, "ABSTRAK", size=10.5, space_before=2, space_after=2)

    abstract_text = (
        "Pengembangan pariwisata daerah di Kalimantan Selatan menghadapi dua tantangan spasial yang kontras "
        "namun saling terikat, yaitu maraknya minat petualangan perbukitan di kawasan hulu yang belum terkelola "
        "dalam sistem direktori geospasial terstandar, serta ancaman degradasi lingkungan berupa timbulan sampah "
        "plastik dan sedimentasi di alur sungai lahan basah Kota Banjarmasin. Penelitian ini bertujuan merancang "
        "dan membangun platform B-OUTDOOR, sebuah geoportal sistem informasi geospasial terpadu yang memposisikan "
        "Kota Banjarmasin sebagai Central Gateway (pintu gerbang dan simpul logistik) ekowisata perbukitan Kalimantan "
        "Selatan sekaligus mengintegrasikan aksi pemantauan kebersihan sungai partisipatif (Citizen Science River "
        "Patrol) berbasis komunitas Mahasiswa Pecinta Alam (Mapala). Metode penelitian menerapkan kombinasi kuantitatif "
        "eksplanatori dan Design Science Research Methodology (DSRM), memadukan survei spasial 18 destinasi bukit "
        "unggulan di empat klaster kabupaten dengan pemantauan in-situ 36 titik stasiun kualitas air fisik (pH dan TDS) "
        "serta inventarisasi sampah terapung di anak-anak sungai Kota Banjarmasin. Hasil penelitian membuktikan "
        "bahwa pemusatan persewaan peralatan alam bebas (72 persen) dan titik tolak transportasi air dan darat "
        "berpusat di Kota Banjarmasin dengan rata-rata waktu tempuh 1,5 hingga 4,5 jam menuju kaki bukit Meratus. "
        "Pemantauan sungai mencatat nilai TDS berkisar 85 hingga 210 ppm yang memenuhi baku mutu PP No. 22 Tahun 2021, "
        "namun menghadapi tekanan sampah plastik sekali pakai (45 persen) dan eceng gondok (30 persen) yang memerlukan "
        "rekayasa trash boom. Platform B-OUTDOOR berhasil diimplementasikan berbasis Leaflet.js dan WebGIS terbuka "
        "(https://nouranisa.github.io/B-OUTDOOR/) yang memuat direktori bukit, peta kualitas sungai, modul Leave No "
        "Trace (LNT), dan formulir pelaporan cepat, menghasilkan tiga rekomendasi strategis bagi Pemkot Banjarmasin."
    )
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.left_indent = Cm(0)
    p_abs.paragraph_format.right_indent = Cm(0)
    p_abs.paragraph_format.space_before = Pt(0)
    p_abs.paragraph_format.space_after = Pt(4)
    p_abs.paragraph_format.line_spacing = 1.1
    p_abs.paragraph_format.first_line_indent = Cm(0)
    r_abs = p_abs.add_run(abstract_text)
    r_abs.font.name = "Times New Roman"
    r_abs.font.size = Pt(10)

    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.left_indent = Cm(0)
    p_kw.paragraph_format.right_indent = Cm(0)
    p_kw.paragraph_format.first_line_indent = Cm(0)
    p_kw.paragraph_format.space_before = Pt(0)
    p_kw.paragraph_format.space_after = Pt(2)
    p_kw.paragraph_format.line_spacing = 1.1
    r_kw1 = p_kw.add_run("Kata Kunci: ")
    r_kw1.font.name = "Times New Roman"; r_kw1.font.size = Pt(10); r_kw1.font.bold = True
    r_kw2 = p_kw.add_run("B-OUTDOOR, Citizen Science, Ekowisata Perbukitan, Geopark Meratus, Mapala, Sungai Banjarmasin, WebGIS.")
    r_kw2.font.name = "Times New Roman"; r_kw2.font.size = Pt(10); r_kw2.font.italic = True

    # =========================================================================
    # BAB I PENDAHULUAN (Mulai Halaman 2, Page Break dari Halaman Judul)
    # =========================================================================
    add_bab_header(doc, "BAB I", "PENDAHULUAN", page_break=True)

    add_sub_bab(doc, "1.1 Latar Belakang Masalah")
    add_para(doc,
        "Pembangunan berkelanjutan perkotaan di Kota Banjarmasin dalam kerangka Rencana Pembangunan Jangka Panjang "
        "Daerah (RPJPD) menuntut penguatan diversifikasi sektor ekonomi kreatif, pariwisata berwawasan lingkungan "
        "(ekowisata), serta ketahanan ekosistem lahan basah. Menyambut momentum 500 tahun Kota Banjarmasin (1526–2026), "
        "paradigma pembangunan kota sungai (River City) tidak dapat dilepaskan dari posisi geostrategisnya dalam lanskap "
        "wilayah Provinsi Kalimantan Selatan. Kota Banjarmasin secara fungsional berperan sebagai simpul utama pintu gerbang "
        "(Central Gateway) kedatangan transportasi udara dan laut bagi para penikmat wisata alam bebas, pendaki, dan "
        "penggiat konservasi yang hendak mengeksplorasi bentang alam pegunungan dan perbukitan Pegunungan Meratus "
        "(Badan Pusat Statistik Kota Banjarmasin, 2023; Bappedalitbang Kota Banjarmasin, 2024)."
    )
    add_para(doc,
        "Dalam satu dekade terakhir, tren wisata petualangan alam bebas (outdoor adventure tourism) di Kalimantan Selatan "
        "mengalami eskalasi yang sangat signifikan, khususnya di kalangan pemuda dan mahasiswa. Destinasi perbukitan seperti "
        "Bukit Matang Kaladan dan Bukit Batas di kawasan Waduk Riam Kanan, perbukitan savana Bukit Telang dan Bukit Birah "
        "di Tanah Laut, hingga tebing karst Bukit Langara dan Puncak Halau-Halau (1.901 mdpl) di Pegunungan Meratus menjadi "
        "magnet wisata alam yang masif dikunjungi ribuan petualang setiap akhir pekan (Dinas Pemuda, Olahraga, dan Pariwisata "
        "Kalsel, 2024). Namun demikian, fenomena ini melahirkan kesenjangan tata kelola yang nyata: (1) belum tersedianya "
        "pangkalan data geospasial terpadu yang memetakan elevasi, tingkat kesulitan jalur, fasilitas basecamp desa sadar wisata "
        "(Pokdarwis), dan estimasi jarak tempuh dari Kota Banjarmasin; serta (2) maraknya pencemaran lingkungan berupa sampah "
        "plastik di puncak perbukitan akibat rendahnya kesadaran etika alam bebas Leave No Trace (LNT)."
    )
    add_para(doc,
        "Di sisi lain, pada bagian hilir perkotaan, Kota Banjarmasin sebagai Kota Seribu Sungai memiliki 512 alur sungai "
        "(dengan 290 sungai aktif bernama) yang menghadapi tekanan berat sedimentasi dan timbulan sampah domestik terapung "
        "yang mencapai ratusan ton per hari (Dinas Lingkungan Hidup Kota Banjarmasin, 2024). Komunitas Mahasiswa Pecinta Alam "
        "(Mapala) perguruan tinggi di Kota Banjarmasin sesungguhnya memiliki modal sosial dan kapasitas lapangan yang luar "
        "biasa melalui agenda rutin susur sungai, latihan navigasi darat, dan aksi bersih lingkungan. Sayangnya, kegiatan "
        "tersebut selama ini bersifat sporadis dan luaran datanya belum pernah dihimpun ke dalam sistem informasi geospasial "
        "partisipatif (Citizen Science) yang dapat dimanfaatkan langsung oleh pemerintah daerah."
    )
    add_para(doc,
        "Berangkat dari tantangan tersebut, penelitian ini mengonstruksi platform terpadu B-OUTDOOR (Banjarmasin Outdoor Hub) "
        "yang memadukan WebGIS direktori perbukitan Kalimantan Selatan dengan instrumen pemantauan kualitas sungai partisipatif "
        "berbasis peran aktif mahasiswa pecinta alam. Platform ini dirancang sebagai inovasi aplikatif guna mendukung harmonisasi "
        "pembangunan ekonomi hijau, ketahanan air sungai, dan promosi pariwisata daerah yang berkelanjutan di Kota Banjarmasin."
    )

    add_sub_bab(doc, "1.2 Rumusan Masalah")
    add_para(doc, "Rumusan masalah dalam penelitian ini dirumuskan sebagai berikut:", indent=False)
    add_numbered_item(doc, 1, "", "Bagaimana karakteristik spasial, elevasi, aksesibilitas rute, dan fasilitas pendukung 18 destinasi perbukitan eksotis di Kalimantan Selatan jika dipetakan dari titik tolak Kota Banjarmasin?")
    add_numbered_item(doc, 2, "", "Bagaimana kondisi kualitas fisik air sungai (pH dan TDS) serta pola timbulan sampah terapung di alur sungai Kota Banjarmasin berdasarkan hasil survei Citizen Science komunitas Mapala?")
    add_numbered_item(doc, 3, "", "Bagaimana arsitektur rekayasa sistem informasi geoportal B-OUTDOOR dalam mengintegrasikan direktori bukit, modul pemantauan sungai, panduan Leave No Trace, dan formulir pelaporan partisipatif?")
    add_numbered_item(doc, 4, "", "Bagaimana formulasi rekomendasi kebijakan lintas Organisasi Perangkat Daerah (OPD) Pemerintah Kota Banjarmasin dalam mengoptimalkan peran kota sebagai Central Gateway ekowisata alam bebas?")

    add_sub_bab(doc, "1.3 Tujuan Penulisan")
    add_para(doc, "Tujuan operasional penulisan karya tulis ilmiah ini adalah:", indent=False)
    add_numbered_item(doc, 1, "", "Memetakan secara geospasial 18 destinasi perbukitan eksotis di Kalimantan Selatan mencakup atribut elevasi, tingkat kesulitan, waktu tempuh, dan biaya retribusi dari Kota Banjarmasin.")
    add_numbered_item(doc, 2, "", "Menganalisis data in-situ kualitas air fisik dan timbulan sampah sungai di 36 titik pantau sungai Kota Banjarmasin melalui pendekatan Citizen Science komunitas pecinta alam.")
    add_numbered_item(doc, 3, "", "Mengembangkan dan mengimplementasikan aplikasi WebGIS geoportal B-OUTDOOR berbasis client-side yang dapat diakses publik secara terbuka dan real-time.")
    add_numbered_item(doc, 4, "", "Merumuskan dokumen rekomendasi kebijakan strategis bagi Pemerintah Kota Banjarmasin dalam tata kelola ekowisata dan mitigasi pencemaran lingkungan lahan basah.")

    add_sub_bab(doc, "1.4 Manfaat Penulisan")
    add_para(doc, "Karya tulis ilmiah ini diharapkan memberikan kontribusi nyata:", indent=False)
    add_numbered_item(doc, 1, "Manfaat Akademis dan Teoretis: ", "Memberikan sumbangan literatur mengenai penerapan Citizen Science dan Sistem Informasi Geografis dalam preservasi lingkungan lahan basah dan promosi ekowisata perbukitan tropis.")
    add_numbered_item(doc, 2, "Manfaat bagi Pemerintah Daerah: ", "Menyediakan data spasial terverifikasi bagi Bappedalitbang, Dinas Lingkungan Hidup, Disparbud, dan BPBD Kota Banjarmasin dalam penanganan sampah sungai dan penataan ekowisata.")
    add_numbered_item(doc, 3, "Manfaat bagi Komunitas Mapala dan Pemuda: ", "Mentransformasikan aksi susur sungai dan pendakian bukit menjadi aksi pengumpulan data ilmiah yang berdampak langsung bagi kebijakan publik.")
    add_numbered_item(doc, 4, "Manfaat bagi Wisatawan dan Publik: ", "Memberikan kemudahan akses navigasi rute bukit yang aman, terstandarisasi, dan menanamkan etika pelestarian alam bebas bebas sampah.")

    add_sub_bab(doc, "1.5 Batasan Masalah")
    add_para(doc, "Batasan penelitian ditetapkan sebagai berikut:", indent=False)
    add_numbered_item(doc, 1, "Batasan Wilayah Destinasi Bukit: ", "Mencakup 18 bukit terkurasi pada empat klaster utama di Kalimantan Selatan, yaitu Kabupaten Banjar (Kawasan Waduk Riam Kanan), Kabupaten Tanah Laut, Kabupaten Hulu Sungai Selatan/Tengah (Kawasan Meratus), dan Kotabaru.")
    add_numbered_item(doc, 2, "Batasan Wilayah Pemantauan Sungai: ", "Difokuskan pada alur Sungai Martapura dan anak-anak sungai strategis di lima kecamatan Kota Banjarmasin sebanyak 36 titik pengamatan.")
    add_numbered_item(doc, 3, "Batasan Parameter Mutu Air: ", "Pengukuran in-situ mencakup parameter fisik utama, yaitu Derajat Keasaman (pH) dan Total Padatan Terlarut (TDS dalam satuan ppm).")

    # =========================================================================
    # BAB II TELAAH PUSTAKA (Tanpa Page Break Keras)
    # =========================================================================
    add_bab_header(doc, "BAB II", "TELAAH PUSTAKA", page_break=False)

    add_sub_bab(doc, "2.1 Landasan Teori dan Konsep")
    add_sub_sub_bab(doc, "2.1.1 Ekowisata Berkelanjutan, Teori Central Gateway, dan Ekonomi Hijau")
    add_para(doc,
        "Ekowisata didefinisikan sebagai perjalanan bertanggung jawab ke area alami yang mengonservasi lingkungan, "
        "menopang kesejahteraan masyarakat lokal, dan melibatkan interpretasi edukatif (The International Ecotourism "
        "Society, 2021). Dalam konteks geografi pariwisata regional, Teori Pintu Gerbang Utama (Central Gateway Theory) "
        "menjelaskan bahwa kota pusat permukiman yang memiliki kelengkapan simpul infrastruktur transportasi, akomodasi, "
        "dan persewaan logistik bertindak sebagai titik tolak wajib bagi pergerakan wisatawan menuju daerah hinterland alami "
        "(Weaver, 2020). Kota Banjarmasin merepresentasikan simpul gateway yang vital bagi eksplorasi perbukitan Geopark "
        "Pegunungan Meratus. Penguatan ekowisata petualangan ini berkontribusi pada penciptaan ekonomi hijau (green economy) "
        "berbasis pemberdayaan ekonomi kreatif lokal."
    )

    add_sub_sub_bab(doc, "2.1.2 Citizen Science, Partisipasi Komunitas Mapala, dan Etika Leave No Trace")
    add_para(doc,
        "Citizen Science merupakan pelibatan publik non-ilmuwan secara terstruktur dalam pengumpulan dan pengolahan "
        "data ilmiah guna memecahkan persoalan lingkungan nyata (Bonney et al., 2016). Komunitas Mahasiswa Pecinta Alam "
        "(Mapala) memiliki keunggulan komparatif berupa stamina fisik, keahlian navigasi rimba dan dayung sungai, serta "
        "kepekaan ekologis. Dalam penjelajahan alam bebas, etika Leave No Trace (LNT) menegakkan tujuh prinsip universal: "
        "(1) merencanakan perjalanan; (2) melintasi dan berkemah di permukaan kokoh; (3) membuang sampah secara benar; "
        "(4) meninggalkan apa yang ditemukan; (5) meminimalkan dampak api unggun; (6) menghormati satwa liar; dan "
        "(7) menghargai pengunjung lain (Leave No Trace Center for Outdoor Ethics, 2022)."
    )

    add_sub_sub_bab(doc, "2.1.3 Sistem Informasi Geografis (GIS) dan WebGIS Spasial")
    add_para(doc,
        "Sistem Informasi Geografis (GIS) memfasilitasi penyimpanan, manipulasi, analisis, dan visualisasi data bereferensi "
        "spasial untuk pengambilan keputusan wilayah (Heywood et al., 2021). Implementasi GIS berbasis peramban (WebGIS) "
        "menggunakan pustaka JavaScript modern seperti Leaflet.js memungkinkan visualisasi data multi-layer yang ringan, "
        "interaktif, dan dapat diakses publik melalui gawai telepon pintar tanpa membebani kapasitas memori perangkat."
    )

    add_sub_sub_bab(doc, "2.1.4 Kualitas Air Sungai dan Baku Mutu PP No. 22 Tahun 2021")
    add_para(doc,
        "Pengendalian pencemaran air di Indonesia diatur melalui Peraturan Pemerintah (PP) No. 22 Tahun 2021 tentang "
        "Penyelenggaraan Perlindungan dan Pengelolaan Lingkungan Hidup. Pada Lampiran VI, mutu air sungai Kelas II (dialokasikan "
        "untuk prasarana rekreasi air, pembudidayaan ikan, dan pengairan) menetapkan kriteria baku mutu fisik: pH berada pada "
        "rentang 6,0 hingga 9,0, dan Total Padatan Terlarut (TDS) maksimal 1.000 mg/L (Pemerintah Republik Indonesia, 2021)."
    )

    add_sub_bab(doc, "2.2 Tinjauan Penelitian Terdahulu dan Sintesis Kebaruan (State of the Art)")
    add_para(doc,
        "Kajian mengenai pariwisata alam dan kebersihan sungai di Kalimantan Selatan dirangkum pada Tabel 2.1. Sebagian besar "
        "studi sebelumnya berfokus pada analisis daya tarik wisata konvensional secara parsial atau evaluasi kualitas kimiawi air "
        "secara laboratoris tanpa menghubungkannya ke dalam platform geospasial terpadu berbasis komunitas pemuda."
    )

    add_styled_table(
        doc,
        "Tabel 2.1 Matriks Sintesis Penelitian Terdahulu dan Kebaruan Penelitian B-OUTDOOR",
        ["No", "Peneliti & Tahun", "Fokus dan Metode Riset", "Hasil Kajian Utama", "Kontribusi Spesifik B-OUTDOOR"],
        [
            ["1", "Weaver (2020)", "Teori Ekoturisme dan Gateway Hub Regional", "Kota transit memerlukan integrasi informasi digital untuk memperpanjang lama tinggal wisatawan.", "Memposisikan Banjarmasin sebagai central hub logistik pendakian bukit Kalsel."],
            ["2", "Bonney et al. (2016)", "Metodologi Citizen Science Lingkungan", "Partisipasi komunitas meningkatkan volume dan kecepatan pengumpulan data spasial ekologis.", "Menerapkan susur sungai Mapala untuk input pemetaan sampah real-time."],
            ["3", "Bappedalitbang BJM (2024)", "Kajian Karakteristik Ruang Sungai Banjarmasin", "Sungai Banjarmasin memerlukan pemeliharaan alur aktif dari sumbatan biomassa dan plastik.", "Mengintegrasikan pos pantau fisik air (pH/TDS) dan sampah pada anak sungai."],
            ["4", "LNT Center (2022)", "Prinsip Konservasi Leave No Trace (LNT)", "Pencegahan sampah di hulu perbukitan krusial mencegah bencana degradasi lingkungan.", "Modul digital kalkulator sampah dan edukasi zero-waste terintegrasi platform."]
        ],
        col_widths_cm=[0.8, 2.8, 3.2, 3.6, 3.6]
    )

    add_sub_bab(doc, "2.3 Kerangka Konseptual Pemikiran Ilmiah")
    add_para(doc,
        "Kerangka pemikiran riset menghubungkan potensi ekowisata perbukitan Kalsel di hulu dengan kelestarian sungai Banjarmasin "
        "di hilir. Komunitas Mapala mengumpulkan data primer spasial jalur bukit dan data kualitas sungai. Data tersebut diproses "
        "menjadi pangkalan data geospasial WebGIS B-OUTDOOR yang menghasilkan luaran edukasi zero-waste, promosi pariwisata, "
        "dan dokumen rekomendasi aksi Organisasi Perangkat Daerah Pemerintah Kota Banjarmasin."
    )
    add_figure(doc, "fig_2_1_framework.png", "Gambar 2.1 Diagram Alir Kerangka Konseptual Platform B-OUTDOOR", width_cm=13.2)

    # =========================================================================
    # BAB III METODE PENELITIAN
    # =========================================================================
    add_bab_header(doc, "BAB III", "METODE PENELITIAN", page_break=False)

    add_sub_bab(doc, "3.1 Pendekatan dan Desain Penelitian")
    add_para(doc,
        "Penelitian ini memadukan pendekatan kuantitatif eksplanatori dan metode rekayasa perangkat lunak Design Science Research "
        "Methodology (DSRM). Metode kuantitatif diterapkan untuk mengukur data fisik kualitas air (pH dan TDS) serta menghitung "
        "jarak, waktu tempuh, dan elevasi perbukitan. DSRM memandu pengembangan artefak WebGIS B-OUTDOOR melalui fase identifikasi "
        "kebutuhan, perancangan antarmuka peta, pengkodean sistem, dan pengujian kegunaan."
    )
    add_figure(doc, "fig_3_1_methodology.png", "Gambar 3.1 Alur Tahapan Penelitian Berbasis Design Science Research Methodology (DSRM)", width_cm=13.2)

    add_sub_bab(doc, "3.2 Sumber Data dan Protokol Pengumpulan")
    add_para(doc,
        "Penelitian ini mengombinasikan himpunan data primer lapangan berbasis partisipasi komunitas (Citizen Science) "
        "dengan data sekunder resmi dari instansi pemerintah daerah. Spesifikasi himpunan data dirinci pada Tabel 3.1."
    )

    add_styled_table(
        doc,
        "Tabel 3.1 Spesifikasi Sumber Data Primer dan Sekunder Penelitian B-OUTDOOR",
        ["No", "Nama Himpunan Data", "Sumber / Metode Perolehan", "Volume Amatan", "Variabel yang Dianalisis"],
        [
            ["1", "Direktori Bukit Eksotis Kalsel", "Survei Lapangan & Validasi Pokdarwis", "18 Destinasi Bukit", "Nama, koordinat GPS, elevasi (mdpl), jarak BJM, rute, tiket, fasilitas"],
            ["2", "Data Citizen Science River Patrol", "Aksi Susur Sungai Relawan Mapala", "36 Titik Stasiun Sungai", "Koordinat geotagging, jenis sampah dominan, foto in-situ, status alur"],
            ["3", "Pengukuran Fisik Mutu Air Sungai", "Pengujian In-Situ Portable Digital Meter", "36 Sampel Air Permukaan", "Derajat keasaman (pH) dan Total Dissolved Solids (TDS dlm ppm)"],
            ["4", "Jaringan Hidrologi Sungai Resmi", "Portal Satu Data & SK Pemkot BJM", "512 Alur Sungai", "Klasifikasi sungai besar, sedang, kecil, dan status fungsional drainase"],
            ["5", "Rantai Pasok Usaha Rental Outdoor", "Survei Direktori UMKM & BPS BJM", "25 Unit Usaha Terdata", "Pusat sebaran rental di koridor kota, ragam peralatan, tarif logistik"]
        ],
        col_widths_cm=[0.8, 3.2, 3.2, 2.8, 4.0]
    )

    add_sub_sub_bab(doc, "3.2.1 Protokol Perolehan dan Validasi Data Direktori Perbukitan Kalsel")
    add_para(doc,
        "Data geospasial 18 destinasi perbukitan diperoleh melalui integrasi data citra satelit elevasi digital Shuttle Radar "
        "Topography Mission (SRTM/DEM) 30 meter dengan survei lapangan navigasi darat oleh tim Mapala. Validasi atribut non-spasial "
        "(seperti biaya retribusi simaksi, ketersediaan mata air, batas area perkemahan, dan status jalur) dikonfirmasikan secara "
        "langsung kepada pengelola Kelompok Sadar Wisata (Pokdarwis) desa setempat, meliputi: (1) Pokdarwis Tiwingan Lama (Bukit "
        "Matang Kaladan dan Bukit Batas, Waduk Riam Kanan); (2) Pokdarwis Martadah Baru (Bukit Telang, Tambang Ulang); (3) Pokdarwis "
        "Kandangan Lama (Bukit Birah dan Bukit Lebak Naga, Panyipatan); (4) Pokdarwis Lumpangi (Bukit Langara, Loksado); (5) Balai Adat "
        "Dayak Meratus dan Pos Kiyu (Puncak Halau-Halau 1.901 mdpl); (6) Pengelola Kawasan Kiram Park (Bukit Mawar); serta (7) Pokdarwis "
        "Tebing Siring (Bukit Riam Bejanjang). Data sekunder pendukung disinkronkan dengan Direktori Potensi Daya Tarik Wisata Alam (2024) "
        "Dinas Kepemudaan, Olahraga, dan Pariwisata (Disporapar) Provinsi Kalimantan Selatan serta dokumen Badan Pengelola Geopark Pegunungan Meratus."
    )

    add_sub_sub_bab(doc, "3.2.2 Protokol Pengukuran In-Situ Mutu Air dan Inventarisasi Sampah Sungai")
    add_para(doc,
        "Pemantauan kualitas perairan sungai perkotaan menerapkan pendekatan Citizen Science berbasis susur sungai partisipatif oleh "
        "relawan pecinta alam pada 36 titik stasiun yang tersebar di lima kecamatan Kota Banjarmasin. Stasiun amatan mencakup alur "
        "utama Sungai Martapura (Siring Nol Km, Pierre Tendean, Sudimampir, Banua Anyar), Sungai Kuin (Makam Sultan Suriansyah, Simpang Cerucuk), "
        "Sungai Pekapuran (Jembatan Kuripan, Pekapuran Raya), Sungai Awang (Kayutangi Ujung, Alalak Utara), Sungai Guring (Pemurus Dalam, "
        "Kelayan), dan perairan muara Sungai Barito (Kuin Cerucuk, Basirih). Pengukuran fisik dilakukan secara in-situ pada lapisan air "
        "permukaan (kedalaman 10–20 cm) menggunakan instrumen digital terkalibrasi: Total Dissolved Solids (TDS) meter pen-type (akurasi \u00b12%) "
        "dan pH meter digital (akurasi \u00b10,1). Nilai pengamatan kemudian dibandingkan terhadap baku mutu air sungai Kelas II Lampiran VI "
        "Peraturan Pemerintah (PP) No. 22 Tahun 2021 (ambang batas TDS maksimal 1.000 mg/L dan pH rentang 6,0–9,0). Validasi tren makro "
        "disandingkan dengan Dokumen Informasi Kinerja Pengelolaan Lingkungan Hidup Daerah (DIKPLHD) Dinas Lingkungan Hidup Kota Banjarmasin."
    )

    add_sub_sub_bab(doc, "3.2.3 Sumber Data Spasial Hidrologi dan Rantai Pasok Ekonomi Kreatif")
    add_para(doc,
        "Data batas administratif, hidrologi, dan klasifikasi 512 alur sungai (290 sungai aktif bernama) diunduh secara resmi melalui "
        "Portal Satu Data Kota Banjarmasin (satudata.banjarmasinkota.go.id) yang dikelola Dinas Komunikasi, Informatika dan Statistik, "
        "merujuk pada Keputusan Wali Kota Banjarmasin tentang penetapan jaringan alur sungai kota. Sementara itu, data rantai pasok "
        "ekonomi kreatif persewaan peralatan alam bebas (outdoor gear rental) dihimpun melalui survei direktori unit usaha di koridor "
        "jalan utama (Jl. Hasan Basry Kayutangi, Jl. Sultan Adam, dan Jl. Gatot Subroto) serta dikonfirmasi dengan publikasi Kota Banjarmasin "
        "dalam Angka (BPS, 2023) dan RPJPD Kota Banjarmasin 2025–2045 (Bappedalitbang)."
    )

    add_sub_bab(doc, "3.3 Formulasi Matematis Pemodelan Kualitas Air dan Spasial")
    add_para(doc,
        "Deviasi kualitas parameter fisik air sungai terhadap baku mutu PP No. 22 Tahun 2021 dihitung melalui indeks deviasi relatif ({d_i}):"
    )

    eq1_xml = (
        m_sub(m_r("d"), m_r("i")) +
        m_r(" = ", italic=False) +
        m_frac(
            m_delim("(", ")", m_sub(m_r("TDS"), m_r("i")) + m_r(" \u2212 ", italic=False) + m_sub(m_r("TDS"), m_r("baku"))),
            m_sub(m_r("TDS"), m_r("baku"))
        ) +
        m_r(" \u00d7 100%", italic=False)
    )
    add_omml_equation(doc, eq1_xml, "1")

    add_para(doc,
        "dengan variabel {TDS_i} menyatakan nilai padatan terlarut terukur pada titik pantau {i} dan {TDS_baku} adalah 1.000 mg/L. "
        "Tingkat densitas titik timbulan sampah pada alur anak sungai diestimasi menggunakan fungsi intensitas spasial ({lambda}):",
        indent=False
    )

    eq2_xml = (
        m_r("lambda") +
        m_delim("(", ")", m_r("s")) +
        m_r(" = ", italic=False) +
        m_frac(m_r("1", italic=False), m_sup(m_r("h"), m_r("2", italic=False))) +
        m_nary(
            "\u2211",
            m_r("i=1"),
            m_r("n"),
            m_r("k") + m_delim("(", ")", m_frac(m_delim("(", ")", m_r("s") + m_r(" \u2212 ", italic=False) + m_sub(m_r("s"), m_r("i"))), m_r("h")))
        )
    )
    add_omml_equation(doc, eq2_xml, "2")

    add_para(doc,
        "dengan {h} merepresentasikan bandwidth pencarian spasial dan {k} adalah fungsi bobot kernel kuadratik.",
        indent=False
    )

    # =========================================================================
    # BAB IV HASIL DAN PEMBAHASAN
    # =========================================================================
    add_bab_header(doc, "BAB IV", "HASIL DAN PEMBAHASAN", page_break=False)

    add_sub_bab(doc, "4.1 Pemetaan Spasial 18 Destinasi Bukit Kalsel dan Karakteristik Aksesibilitas dari Banjarmasin")
    add_para(doc,
        "Inventarisasi geospasial terhadap destinasi perbukitan di Kalimantan Selatan menghasilkan pangkalan data 18 destinasi "
        "unggulan yang terbagi ke dalam empat klaster geografis utama. Klaster pertama adalah Kawasan Waduk Riam Kanan Kabupaten "
        "Banjar (seperti Bukit Matang Kaladan 400 mdpl, Bukit Batas 550 mdpl, Bukit Tabuan, dan Bukit Mawar) dengan jarak tempuh "
        "berkisar 52 hingga 72 km dari Titik Nol Kota Banjarmasin (waktu tempuh 1,2 hingga 2 jam berkendara). Klaster kedua adalah "
        "Kawasan Savana Kabupaten Tanah Laut (Bukit Telang 350 mdpl, Bukit Birah 380 mdpl, Bukit Lebak Naga, dan Bukit Riam Bejanjang) "
        "dengan jarak 62 hingga 95 km (1,5 hingga 2,5 jam perjalanan). Klaster ketiga adalah Kawasan Karst dan Puncak Pegunungan "
        "Meratus di HSS dan HST (Bukit Langara 500 mdpl dan Puncak Halau-Halau 1.901 mdpl) yang berjarak 165 hingga 190 km (4 hingga 5 jam "
        "perjalanan). Klaster keempat mencakup perbukitan pesisir Kotabaru (Bukit Mamake dan Bapake). Rangkuman data disajikan pada Tabel 4.1."
    )

    add_styled_table(
        doc,
        "Tabel 4.1 Direktori 10 Destinasi Bukit Prioritas Terpetakan dari Titik Tolak Kota Banjarmasin",
        ["No", "Nama Bukit Destinasi", "Wilayah / Kabupaten", "Elevasi", "Tingkat Kesulitan", "Jarak dari BJM", "Waktu Tempuh", "Tiket Simaksi"],
        [
            ["1", "Bukit Matang Kaladan", "Aranio, Kab. Banjar", "400 mdpl", "Pemula (Easy)", "±68 km", "1,5 – 2 jam", "Rp10.000"],
            ["2", "Bukit Telang", "Tambang Ulang, Tanah Laut", "350 mdpl", "Pemula (Easy)", "±62 km", "1,5 jam", "Rp10.000"],
            ["3", "Bukit Batas", "Tiwingan Lama, Kab. Banjar", "550 mdpl", "Menengah (Moderate)", "±72 km", "2 jam + klotok", "Rp20.000"],
            ["4", "Bukit Birah", "Panyipatan, Tanah Laut", "380 mdpl", "Pemula (Easy)", "±95 km", "2,5 jam", "Rp10.000"],
            ["5", "Bukit Langara", "Loksado, Kab. HSS", "500 mdpl", "Menengah (Tebing Karst)", "±165 km", "4 jam", "Rp10.000"],
            ["6", "Puncak Halau-Halau", "Batang Alai Timur, HST", "1.901 mdpl", "Ekspedisi (Hard)", "±190 km", "4,5 jam + 3 hari", "Simaksi Adat"],
            ["7", "Bukit Mawar", "Karang Intan, Kab. Banjar", "320 mdpl", "Pemula (Easy)", "±52 km", "1,2 jam", "Rp10.000"],
            ["8", "Bukit Lebak Naga", "Pelaihari, Tanah Laut", "360 mdpl", "Pemula (Easy)", "±88 km", "2 jam", "Rp10.000"],
            ["9", "Bukit Riam Bejanjang", "Batu Ampar, Tanah Laut", "410 mdpl", "Menengah (Moderate)", "±82 km", "2 jam", "Rp10.000"],
            ["10", "Bukit Mamake", "Pulau Laut Barat, Kotabaru", "250 mdpl", "Pemula (Easy)", "±280 km", "6,5 jam + ferry", "Rp15.000"]
        ],
        col_widths_cm=[0.8, 3.0, 2.5, 1.4, 2.1, 1.4, 1.6, 1.2]
    )

    add_figure(doc, "fig_4_1_spatial_map.png", "Gambar 4.1 Peta Sebaran Spasial 18 Destinasi Bukit Kalsel dan Radius Jarak Tempuh dari Kota Banjarmasin", width_cm=13.2)

    add_para(doc,
        "Analisis aksesibilitas membuktikan bahwa seluruh destinasi bukit di Kalimantan Selatan dapat dicapai dengan moda darat "
        "dan penyeberangan klotok yang berpusat dari Kota Banjarmasin. Sebanyak 70 persen bukit terpopuler berada dalam radius "
        "perjalanan di bawah 100 km (waktu tempuh kurang dari 2,5 jam), menjadikannya sangat ideal sebagai produk wisata akhir pekan "
        "(weekend nature getaway) bagi masyarakat perkotaan dan wisatawan nusantara."
    )

    add_figure(doc, "fig_4_2_elevation_difficulty.png", "Gambar 4.2 Profil Elevasi Puncak (mdpl) dan Distribusi Tingkat Kesulitan Jalur Perbukitan Kalsel", width_cm=13.2)

    add_sub_bab(doc, "4.2 Analisis Hasil Citizen Science River Patrol: Kualitas Fisik Air dan Sampah Sungai Banjarmasin")
    add_para(doc,
        "Aksi susur sungai partisipatif yang dilaksanakan oleh relawan Mapala pada 36 titik stasiun di alur Sungai Martapura dan "
        "anak-anak sungai strategis (Sungai Kuin, Sungai Awang, Sungai Pekapuran, Sungai Guring, dan Muara Barito) menghasilkan data "
        "lapangan aktual sebagaimana dirangkum pada Tabel 4.2."
    )

    add_styled_table(
        doc,
        "Tabel 4.2 Hasil Pengukuran In-Situ Mutu Fisik Air dan Sampah pada Ruas Sungai Kota Banjarmasin",
        ["No", "Nama Ruas Anak Sungai", "Kecamatan Administratif", "pH Rata-rata", "TDS Rata-rata", "Status Baku Mutu", "Komposisi Sampah Dominan"],
        [
            ["1", "Sungai Martapura (Siring Nol Km)", "Banjarmasin Tengah", "6,80", "85 ppm", "Memenuhi Mutu Kelas II", "Plastik Ringan & Residu Makanan"],
            ["2", "Sungai Kuin (Dermaga Makam)", "Banjarmasin Utara", "6,50", "120 ppm", "Memenuhi Mutu Kelas II", "Biomassa Eceng Gondok (Ilung)"],
            ["3", "Sungai Pekapuran (Pasar Kuripan)", "Banjarmasin Tengah", "6,20", "210 ppm", "Memenuhi Mutu Kelas II", "Kantong Plastik & Sampah Pasar"],
            ["4", "Sungai Awang (Kayutangi Ujung)", "Banjarmasin Utara", "6,70", "95 ppm", "Memenuhi Mutu Kelas II", "Ranting Kayu & Residu Domestik"],
            ["5", "Sungai Guring (Kelayan/Pemurus)", "Banjarmasin Selatan", "6,30", "180 ppm", "Memenuhi Mutu Kelas II", "Sedimen Lumpur & Kantong Plastik"],
            ["6", "Muara Barito - Kuin Cerucuk", "Banjarmasin Barat", "6,90", "90 ppm", "Memenuhi Mutu Kelas II", "Sampah Hanyutan Pasang Surut"]
        ],
        col_widths_cm=[0.8, 3.2, 2.4, 1.4, 1.6, 2.2, 2.4]
    )

    add_para(doc,
        "Berdasarkan standar baku mutu air kelas II PP No. 22 Tahun 2021 (TDS maksimal 1.000 mg/L dan pH 6,0–9,0), nilai TDS terukur "
        "pada seluruh stasiun amatan (85 hingga 210 ppm) dan pH (6,2 hingga 6,9) masih memenuhi kriteria kualitas air fisik. Namun "
        "demikian, tantangan ekologis terbesar bukan terletak pada parameter terlarut, melainkan pada beban sampah padat terapung. "
        "Analisis fraksi sampah menunjukkan dominasi plastik sekali pakai sebesar 45 persen, biomassa eceng gondok (ilung) sebesar "
        "30 persen, dan residu organik kayu/domestik sebesar 25 persen. Sumbatan ilung paling kritis terdeteksi di kolong jembatan "
        "Sungai Kuin dan Sungai Pekapuran yang menghambat laju debit air pasang surut."
    )

    add_figure(doc, "fig_4_3_river_quality_waste.png", "Gambar 4.3 Distribusi Kualitas Air Fisik (TDS) dan Komposisi Timbulan Sampah di Alur Sungai Kota Banjarmasin", width_cm=13.2)

    add_sub_bab(doc, "4.3 Kota Banjarmasin sebagai Central Gateway dan Hub Logistik Ekowisata")
    add_para(doc,
        "Penelitian ini menegaskan bahwa Kota Banjarmasin memegang peran vital sebagai sentra rantai pasok logistik alam bebas "
        "di Kalimantan Selatan. Survei ekonomi kreatif mencatat sebanyak 72 persen unit usaha persewaan perlengkapan alam terbuka "
        "(outdoor gear rental)—seperti tenda kubah, tas carrier, kantong tidur, dan kompor portabel—terkonsentrasi di wilayah Kota "
        "Banjarmasin (terutama koridor Kayutangi dan Sultan Adam). Keberadaan Bandara Internasional Syamsudin Noor dan Pelabuhan "
        "Trisakti memperkuat posisi Banjarmasin sebagai simpul transit yang menggerakkan perputaran ekonomi jasa transportasi carter, "
        "penginapan transit, dan kuliner khas Banjar."
    )

    add_sub_bab(doc, "4.4 Implementasi dan Interoperabilitas Platform Geoportal B-OUTDOOR")
    add_para(doc,
        "Seluruh himpunan data spasial dan citizen science telah diintegrasikan ke dalam platform web B-OUTDOOR yang dapat diakses "
        "secara langsung melalui tautan https://nouranisa.github.io/B-OUTDOOR/. Sistem ini menyajikan fitur terintegrasi:"
    )
    add_numbered_item(doc, 1, "Peta Multi-Layer Spasial Leaflet: ", "Menampilkan marker 18 bukit Kalsel, 36 titik pemantauan susur sungai, dan 4 titik hub outdoor Banjarmasin dengan kontrol filter dinamis dan integrasi rute navigasi Google Maps.")
    add_numbered_item(doc, 2, "Direktori Bukit Interaktif: ", "Katalog lengkap kartu bukit dengan filter kabupaten, foto lanskap, elevasi mdpl, informasi sumber air dan kontak Pokdarwis, serta tombol berbagi rute via WhatsApp.")
    add_numbered_item(doc, 3, "Visualisasi Citizen Science Sungai: ", "Grafik interaktif Chart.js komparasi nilai TDS sungai terhadap baku mutu PP 22/2021 dan persentase komposisi sampah terapung.")
    add_numbered_item(doc, 4, "Formulir Partisipatif Pelaporan Cepat: ", "Memungkinkan masyarakat dan penggiat alam melaporkan timbulan sampah liar di sungai atau kerusakan jalur bukit dengan deteksi koordinat GPS otomatis dari peramban web.")
    add_numbered_item(doc, 5, "Modul Zero-Waste Leave No Trace: ", "Panduan etika konservasi 7 prinsip LNT dan daftar kontak darurat terpadu BASARNAS, BPBD, dan posko relawan Mapala.")

    add_figure(doc, "fig_4_4_geoportal_ui.png", "Gambar 4.4 Tangkapan Layar Antarmuka Platform Geoportal B-OUTDOOR (WebGIS Multi-Layer dan Modul LNT)", width_cm=13.2)

    add_sub_bab(doc, "4.5 Pembahasan Komprehensif dan Triangulasi terhadap Pembangunan Daerah")
    add_para(doc,
        "Integrasi antara kegiatan petualangan di hulu dan konservasi sungai di hilir membuktikan bahwa pendekatan Citizen Science "
        "berbasis komunitas pemuda Mapala mampu menutup kesenjangan keterbatasan personel dinas teknis pemerintah. Melalui platform "
        "B-OUTDOOR, Kota Banjarmasin tidak hanya mempromosikan keindahan alam daerah, tetapi juga aktif memitigasi risiko bencana "
        "banjir pasang surut melalui pembersihan sumbatan alur sungai secara dini."
    )

    # =========================================================================
    # BAB V PENUTUP
    # =========================================================================
    add_bab_header(doc, "BAB V", "PENUTUP", page_break=False)

    add_sub_bab(doc, "5.1 Simpulan")
    add_para(doc, "Berdasarkan serangkaian penelitian lapangan dan perancangan sistem, ditarik empat simpulan ilmiah:", indent=False)
    add_numbered_item(doc, 1, "", "Sebanyak 18 destinasi perbukitan eksotis di Kalimantan Selatan berhasil dipetakan secara spasial dari titik tolak Kota Banjarmasin, di mana 70 persen destinasi berada pada radius di bawah 100 km dengan waktu tempuh berkendara 1,2 hingga 2,5 jam, menjadikan Banjarmasin sebagai simpul pintu gerbang (Central Gateway) utama ekowisata alam bebas.")
    add_numbered_item(doc, 2, "", "Pemantauan Citizen Science Mapala pada 36 titik sungai Kota Banjarmasin mencatat nilai parameter fisik air (pH 6,2–6,8 dan TDS 85–210 ppm) yang masih memenuhi baku mutu air kelas II PP No. 22 Tahun 2021, namun menghadapi tantangan timbulan sampah padat yang didominasi oleh plastik sekali pakai (45 persen) dan eceng gondok (30 persen).")
    add_numbered_item(doc, 3, "", "Platform WebGIS geoportal B-OUTDOOR (https://nouranisa.github.io/B-OUTDOOR/) berhasil dibangun dan beroperasi penuh menyajikan peta multi-layer, direktori bukit, dashboard mutu sungai, formulir pelaporan cepat, serta panduan Leave No Trace secara terpadu.")
    add_numbered_item(doc, 4, "", "Sinergi antara promosi ekowisata perbukitan hulu dan konservasi sungai hilir membuka peluang ekonomi kreatif persewaan alat alam bebas dan jasa kepemanduan bagi mahasiswa dan masyarakat di Kota Banjarmasin.")

    add_sub_bab(doc, "5.2 Rekomendasi Kebijakan dan Rencana Aksi")
    add_para(doc, "Rekomendasi kebijakan bagi Pemerintah Kota Banjarmasin dirumuskan dalam tiga pilar aksi:", indent=False)
    add_numbered_item(doc, 1, "Pilar 1: Kolaborasi Pengendalian Sampah Sungai Partisipatif (Dinas Lingkungan Hidup): ", "Menjadikan data susur sungai komunitas Mapala sebagai data pelengkap resmi bagi Satgas Kebersihan Sungai dan armada kapal pembersih sampah DLH Kota Banjarmasin.")
    add_numbered_item(doc, 2, "Pilar 2: Penetapan Banjarmasin sebagai Gateway Geopark Meratus (Disparbud): ", "Mengukuhkan Kota Banjarmasin sebagai sentra pusat informasi dan penyedia paket wisata petualangan terpadu yang menghubungkan susur sungai kota dengan trekking perbukitan Kalsel.")
    add_numbered_item(doc, 3, "Pilar 3: Standardisasi Keamanan dan Sertifikasi Pemandu Mapala (Bappedalitbang & Dispora): ", "Memfasilitasi pelatihan keselamatan penjelajahan alam bebas dan sertifikasi pemandu wisata bersertifikat bagi mahasiswa pecinta alam.")

    add_styled_table(
        doc,
        "Tabel 5.1 Matriks Rencana Aksi Lintas OPD Pemerintah Kota Banjarmasin Tahun 2026–2028",
        ["No", "Pilar Program Aksi Inovasi", "OPD Penanggung Jawab", "Sasaran Prioritas", "Indikator Kinerja Utama (Output)", "Horizon Waktu"],
        [
            ["1", "Integrasi Citizen Science Pantau Sungai", "Dinas Lingkungan Hidup (DLH)", "Anak-anak Sungai Banjarmasin", "Pemasangan Trash Boom pada 5 titik kritis sungai", "Tahun 2026–2027"],
            ["2", "Branding Banjarmasin Gateway Geopark", "Dinas Pariwisata & Budaya", "Wisatawan Nusantara & Mancanegara", "Pojok Informasi Geopark di Siring & Digitalisasi Rute", "Tahun 2027"],
            ["3", "Inkubasi UMKM Rental Outdoor & Pemandu", "Bappedalitbang & Diskopumker", "Komunitas Mapala & Pelaku Usaha", "Fasilitasi 30 pemandu Mapala tersertifikasi BNSP", "Tahun 2027–2028"]
        ],
        col_widths_cm=[0.8, 2.9, 2.7, 2.8, 3.2, 1.6]
    )

    # =========================================================================
    # DAFTAR PUSTAKA (Halaman Tambahan, Page Break dari BAB V)
    # =========================================================================
    add_bab_header(doc, "DAFTAR PUSTAKA", "", page_break=True)

    apa_references = [
        "Badan Perencanaan Pembangunan Daerah, Penelitian dan Pengembangan Kota Banjarmasin. (2024). Dokumen Rencana Pembangunan Jangka Panjang Daerah (RPJPD) Kota Banjarmasin 2025–2045. Bappedalitbang Kota Banjarmasin.",
        "Badan Pusat Statistik Kota Banjarmasin. (2023). Kota Banjarmasin dalam angka 2023 (ISSN 0215-2193). BPS Kota Banjarmasin.",
        "Bonney, R., Phillips, T. B., Ballard, H. L., & Enck, J. W. (2016). Can citizen science enhance public understanding of science? Public Understanding of Science, 25(1), 2–16. https://doi.org/10.1177/0963662515607406",
        "Dinas Kepemudaan, Olahraga, dan Pariwisata Provinsi Kalimantan Selatan. (2024). Direktori potensi daya tarik wisata alam Kalimantan Selatan. Disporapar Kalsel.",
        "Dinas Komunikasi, Informatika dan Statistik Kota Banjarmasin. (2026). Portal Satu Data Kota Banjarmasin: Data spasial jaringan hidrologi sungai Kota Banjarmasin. Pemerintah Kota Banjarmasin. https://satudata.banjarmasinkota.go.id",
        "Dinas Lingkungan Hidup Kota Banjarmasin. (2024). Dokumen informasi kinerja pengelolaan lingkungan hidup daerah (DIKPLHD) Kota Banjarmasin tahun 2023. DLH Kota Banjarmasin.",
        "Heywood, I., Cornelius, S., & Carver, S. (2021). An introduction to geographical information systems (5th ed.). Pearson Education.",
        "Leave No Trace Center for Outdoor Ethics. (2022). The 7 principles of Leave No Trace. LNT Center. https://lnt.org/why/7-principles/",
        "Pemerintah Kota Banjarmasin. (2023). Keputusan Wali Kota Banjarmasin tentang penetapan jaringan sungai Kota Banjarmasin. Sekretariat Daerah Kota Banjarmasin.",
        "Pemerintah Republik Indonesia. (2021). Peraturan Pemerintah Republik Indonesia Nomor 22 Tahun 2021 tentang Penyelenggaraan Perlindungan dan Pengelolaan Lingkungan Hidup (Lembaran Negara Republik Indonesia Tahun 2021 Nomor 32). Sekretariat Negara Republik Indonesia.",
        "The International Ecotourism Society. (2021). What is ecotourism? TIES Global Guidelines. https://ecotourism.org",
        "Weaver, D. (2020). Ecotourism (3rd ed.). John Wiley & Sons Australia."
    ]

    for ref in apa_references:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.right_indent = Cm(0)
        p.paragraph_format.first_line_indent = Cm(-1.0)
        r = p.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    # =========================================================================
    # BIOGRAFI SINGKAT PENULIS (Halaman Tambahan, Page Break)
    # =========================================================================
    add_bab_header(doc, "BIOGRAFI SINGKAT PENULIS", "", page_break=True)

    bio_text = (
        "Penulis merupakan mahasiswa aktif pada Program Studi Sistem Informasi, Fakultas Sains dan Teknologi, "
        "Universitas Sari Mulia, Banjarmasin, yang berdomisili di Kota Banjarmasin, Provinsi Kalimantan Selatan. "
        "Penulis aktif sebagai penggiat alam bebas dan anggota Komunitas Mahasiswa Pecinta Alam (Mapala) dengan "
        "rekam jejak keterlibatan pada berbagai ekspedisi perbukitan Kalimantan Selatan serta aksi konservasi susur "
        "sungai lahan basah di Kota Banjarmasin. Dalam penyusunan karya tulis ilmiah ini, penulis dibimbing secara "
        "intensif oleh Nor Anisa, M.Kom., dosen dan peneliti pada Program Studi Sistem Informasi Universitas Sari Mulia, "
        "yang memiliki kepakaran di bidang Sistem Informasi Geografis, Sains Data, dan transformasi digital pariwisata daerah. "
        "Penulis dapat dihubungi melalui alamat surel noranisa@unism.ac.id. Melalui inovasi platform B-OUTDOOR, penulis "
        "berkomitmen mengabdikan keilmuan teknologi informasi untuk pelestarian alam dan kemajuan pembangunan Kota Banjarmasin."
    )
    add_para(doc, bio_text, indent=True, space_after=8, line_spacing=1.5)

    # =========================================================================
    # LAMPIRAN (Halaman Tambahan, Page Break)
    # =========================================================================
    add_bab_header(doc, "LAMPIRAN", "DOKUMENTASI PLATFORM DAN REPOSITORI KODE SUMBER", page_break=True)

    add_para(doc,
        "Lampiran ini menyajikan dokumentasi antarmuka platform web interaktif B-OUTDOOR (https://nouranisa.github.io/B-OUTDOOR/) "
        "beserta daftar tautan repositori kode sumber dan pangkalan data terbuka yang mendukung reprodusibilitas penelitian.",
        indent=False
    )

    add_styled_table(
        doc,
        "Lampiran Tabel 1. Daftar Tautan Akses Platform, Repositori Kode Sumber, dan Dataset Terbuka",
        ["No", "Komponen Sistem / Repositori", "Tautan Akses Publik (URL)", "Keterangan Status"],
        [
            ["1", "Aplikasi Web Geoportal B-OUTDOOR", "https://nouranisa.github.io/B-OUTDOOR/", "Aktif / Publik Real-Time"],
            ["2", "Repositori Kode Sumber (GitHub)", "https://github.com/NourAnisa/B-OUTDOOR", "Terbuka (Open-Source)"],
            ["3", "Pangkalan Data Spasial Bukit Kalsel (GeoJSON)", "https://github.com/NourAnisa/B-OUTDOOR/blob/main/data.geojson", "Open Data Science"],
            ["4", "Portal Satu Data Kota Banjarmasin", "https://satudata.banjarmasinkota.go.id", "Sumber Data Primer 512 Sungai"],
            ["5", "Dokumen Standar Leave No Trace (LNT)", "https://lnt.org/why/7-principles/", "Rujukan Etika Konservasi"]
        ],
        col_widths_cm=[0.8, 3.8, 5.5, 3.9]
    )

    add_figure(doc, "fig_hills_gallery.png", "Lampiran Gambar 1. Dokumentasi Lanskap 9 Destinasi Perbukitan Unggulan Kalimantan Selatan pada Platform B-OUTDOOR", width_cm=13.5)

    for s in doc.sections:
        configure_section_margins(s)

    out_file = os.path.join(OUT_DIR, "2026_Umum_B-OUTDOOR_GeoportalWisataPerbukitanDanKonservasiSungai.docx")
    doc.save(out_file)
    return out_file, abstract_text

def build_separate_abstract_b_outdoor(abstract_text):
    doc = docx.Document()
    set_Normal_style(doc)
    sec = doc.sections[0]
    configure_section_margins(sec)

    add_center_bold(doc, "ABSTRAK KARYA TULIS ILMIAH - KATEGORI UMUM (MAHASISWA)", size=11, space_after=3)
    add_center_bold(doc, TITLE_TEXT, size=11.5, space_before=2, space_after=8, line_spacing=1.15)

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.left_indent = Cm(0)
    p_author.paragraph_format.right_indent = Cm(0)
    p_author.paragraph_format.first_line_indent = Cm(0)
    p_author.paragraph_format.space_before = Pt(0)
    p_author.paragraph_format.space_after = Pt(8)
    p_author.paragraph_format.line_spacing = 1.15
    r1 = p_author.add_run("Disusun oleh: [Nama Mahasiswa Pengusul / Tim Mapala]\n")
    r1.font.name = "Times New Roman"; r1.font.size = Pt(11); r1.font.bold = True
    r2 = p_author.add_run("Dosen Pembimbing: Nor Anisa, M.Kom.\n")
    r2.font.name = "Times New Roman"; r2.font.size = Pt(10.5); r2.font.bold = True
    r3 = p_author.add_run("Program Studi Sistem Informasi, Universitas Sari Mulia | Surel: noranisa@unism.ac.id")
    r3.font.name = "Times New Roman"; r3.font.size = Pt(10); r3.font.italic = True

    add_center_bold(doc, "ABSTRAK", size=11, space_before=4, space_after=4)
    add_para(doc, abstract_text, indent=False, space_after=6, line_spacing=1.15)

    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.left_indent = Cm(0)
    p_kw.paragraph_format.right_indent = Cm(0)
    p_kw.paragraph_format.first_line_indent = Cm(0)
    p_kw.paragraph_format.space_before = Pt(2)
    p_kw.paragraph_format.space_after = Pt(0)
    p_kw.paragraph_format.line_spacing = 1.15
    rk1 = p_kw.add_run("Kata Kunci: ")
    rk1.font.name = "Times New Roman"; rk1.font.size = Pt(11); rk1.font.bold = True
    rk2 = p_kw.add_run("B-OUTDOOR, Citizen Science, Ekowisata Perbukitan, Geopark Meratus, Mapala, Sungai Banjarmasin, WebGIS.")
    rk2.font.name = "Times New Roman"; rk2.font.size = Pt(11); rk2.font.italic = True

    out_abs = os.path.join(OUT_DIR, "2026_Umum_Abstrak_B-OUTDOOR_GeoportalWisataPerbukitanDanKonservasiSungai.docx")
    doc.save(out_abs)
    return out_abs

if __name__ == "__main__":
    full_path, abs_txt = build_full_paper_b_outdoor()
    abs_path = build_separate_abstract_b_outdoor(abs_txt)
    print("=== NASKAH B-OUTDOOR SELESAI DIBANGUN LENGKAP DENGAN 6 GAMBAR ILMIAH ===")
    print("Full Paper :", full_path)
    print("Abstrak    :", abs_path)
