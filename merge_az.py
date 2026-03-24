import os, io
from pypdf import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.units import inch

w, h = letter
repo = '/home/ubuntu/azbar'
ML = 0.85 * inch
MR = w - 0.85 * inch

STRUCTURE = [
    ('section', 'Section I', 'Application and Letters of Recommendation'),
    (1,  '2.5.25_Authorization_&_Release.pdf',                        'Authorization and Release',                                '2025-02-05', '2025-02-05'),
    (2,  '2.5.25_Declaration.pdf',                                     'Declaration',                                              '2025-02-05', '2025-02-05'),
    (3,  '25.2.05_AZ_C&F_Application_Amendment_10.23.25.pdf',          'Character & Fitness Application (Amended)',                 '2025-10-23', '2025-10-23'),
    (4,  'Addendum.pdf',                                               'Addendum to Cure Omissions',                               '2025-10-19', '2025-10-20'),
    (5,  'Character_letter_BJS.pdf',                                   'Brandon Squires Letter of Recommendation',                 '2026-03-18', '2026-03-23'),
    (6,  'LOR- David Nimer AZ Bar.pdf',                                'Tim Myers Letter of Recommendation',                       '2025-10-22', '2025-11-12'),
    ('section', 'Section II', 'Medical and Psychological Evaluations'),
    (7,  'DN LTR AZ SUPREME CT 11-11-25.pdf',                         'Dr. Michael Kerrigan Letter',                              '2025-11-11', '2025-11-12'),
    (8,  '25.10.21_Dr_Manriquez_Letter.pdf',                           'Dr. Maria Manriquez Letter',                               '2025-10-21', '2025-11-12'),
    (9,  '25.12.04_Dr_Brower_Neurospych_Eval.pdf',                     'Dr. Michael Brower Neuropsychological Report',             '2025-12-04', 'n/a'),
    (10, '25.7.18._Dr_Bashah_Psych_Eval.pdf',                          'Dr. Emily Bashah Psychological Evaluation',                '2025-07-18', 'n/a'),
    (11, '18.5.19_Dr_Kerrigan_Neuropsych_Eval.pdf',                    'Dr. Kerrigan Neuropsych Eval (2018)',                      '2018-07-04', '2025-10-31'),
    (12, '16.2.02_Dr_Bradshaw_Menninger_Neuropsych_Eval.pdf',          'Dr. Bradshaw/Menninger Neuropsych Eval (2016)',            '2016-02-04', '2025-10-31'),
    (13, '15.12.04_Dr_Rao_Progress_Note.pdf',                          'Dr. Rao Progress Note (2015)',                             '2015-12-04', '2025-10-31'),
    (14, '15.12.02_Brain_MRI_Report_Dr_Rao.pdf',                       'Brain MRI (Dec. 2015)',                                    '2015-12-02', '2025-10-31'),
    (15, '15.3.12_Brain_MRI_Report_Dr_Rao.pdf',                        'Brain MRI (Mar. 2015)',                                    '2015-03-12', '2025-10-31'),
    (16, '15.2.08_CT+MRI_Brain_OKC.pdf',                               'CT & MRI Brain (Feb. 2015)',                               '2015-02-08', '2025-10-31'),
    ('section', 'Section III', 'Transcripts and University Records'),
    (17, 'Transcript_Arizona_State_Law.pdf',                           'Transcript - ASU',                                         'Class of 2023', '2025-10-20'),
    (18, 'Transcript_Duke.pdf',                                        'Transcript - Duke',                                        'Class of 2020', '2025-10-20'),
    (19, 'Transcript_Colorado.pdf',                                    'Transcript - CU Boulder',                                  'Class of 2015', '2025-10-20'),
    (20, 'Transcript_Dickinson.pdf',                                   'Transcript - Dickinson',                                   '',              '2025-10-20'),
    (21, '21.8.17_ASU_Readmission_Letter.pdf',                         'ASU Readmission',                                          '2021-08-17',    '2025-10-20'),
    (22, '21.7.1_ASU_Disqualification_Letter.pdf',                     'ASU Disqualification',                                     '2021-07-01',    '2025-10-20'),
    (23, '19.5.24_Duke_Academic_Probation_Off_Notice.pdf',             'Duke Academic Probation - Off',                            '2019-05-24',    '2025-10-20'),
    (24, '19.1.14_Duke_Academic_Probation_Notice.pdf',                 'Duke Academic Probation - On',                             '2019-01-04',    '2025-10-20'),
    (25, '25.9.17_Dickinson_Conduct_Records_Letter.pdf',               'Dickinson Conduct Records Letter',                         '2025-09-17',    '2025-10-20'),
    ('section', 'Section IV', 'Driver Records and Court Documents of DUIs'),
    (26, 'Driving_Record_Arizona_12.10.24.pdf',                        'Driving Record [Arizona current]',                         '2024-12-10',    '2025-02-05'),
    (27, 'Driving_Record_North_Carolina_12.10.24.pdf',                 'North Carolina Driving Record (Traffic History #1)',       '2024-12-10',    '2025-01-21'),
    (28, 'Driving_Record_Colorado_12.09.24.pdf',                       'Colorado Driving Record (Traffic History #1)',             '2024-12-09',    '2025-01-21'),
    (29, '17.10.24_Order_to_Seal_16T10.pdf',                           'Disposition [Order to Seal 16T10 (DUID, #3)]',            '2017-10-24',    '2025-01-22'),
    (30, '00001-2017-08-31 - Order to Terminate Probation.pdf',        'Proof of Satisfaction [Order to Terminate Probation]',    '2017-08-31',    '2025-01-22'),
    (31, '00011-2016-06-06 - Mittimus - Issued.pdf',                   'Disposition [Guilty Plea + Sentence 15T2454 (DWAI,#1)]',  '2016-06-06',    '2025-01-22'),
    (32, '00011-2016-10-24 - Completion of Mittimus Sentence.pdf',     'Disposition [Guilty Plea + Sentence 15T2492 (DUI,#2)]',   '2016-06-06',    '2025-01-22'),
    (33, '00014-2016-06-06 - Mittimus - Issued.pdf',                   'Disposition [Concurrent Sentence]',                       '2016-06-06',    '2025-01-22'),
    (34, '00012-2016-06-06 - Plea Agreement.pdf',                      'Sentence [Plea Agreement 15T2454 (DWAI, #1)]',            '2016-06-06',    '2025-01-22'),
    (35, '00013-2016-06-06 - Plea Agreement.pdf',                      'Sentence [Plea Agreement 15T2492 (DUI, #2)]',             '2016-06-06',    '2025-01-22'),
    (36, '00017-2015-09-18 - Summons and Complaint.pdf',               'Complaint/Indictment/Disposition [15T2454 (DWAI,#1)]',    '2015-09-17',    '2025-01-22'),
    (37, '00018-2015-11-16 - Summons and Complaint.pdf',               'Complaint/Indictment/Disposition [15T2492 (DUI,#2)]',     '2015-11-14',    '2025-01-22'),
    (38, '00016-2015-09-18 - Arrest Report.pdf',                       'Police Report [15T2454 (DWAI, #1)]',                      '2015-09-18',    '2025-01-22'),
    (39, '00010-2016-11-16 - Arrest Report.pdf',                       'Police Report [15T2492 (DUI, #2)]',                       '2015-11-16',    '2025-01-22'),
    ('section', 'Section V', 'Traffic Tickets'),
    (40, 'Traffic#1_19.11.15_Washington_Co._Ticket_Disposition.pdf',   'Traffic Case #1 [2019 - speeding]',                       '',              '2025-02-05'),
    (41, 'Traffic#2_18.4.10_Frederick_Ticket_Disposition.pdf',         'Traffic Case #2 [2018 - Speeding 10-19 Over]',            '',              '2025-01-24'),
    (42, 'Traffic#3_17.10.13_Longmont_Ticket_Disposition.pdf',         'Traffic Case #3 [2017 - Signal Light]',                   '',              '2025-01-24'),
    (43, 'Traffic#4_15.10.9_Erie_Ticket_Disposition.pdf',              'Traffic Case #4 [2015 - Failed To Yield]',                '',              '2025-01-24'),
    (44, 'Traffic#5_14.10.26_Kit_Carson_County_Ticket_Disposition.pdf','Traffic Case #5 [2014 - unknown]',                        '',              '2025-01-24'),
    (45, 'Traffic#6_13.8.25_Golden_Ticket_Disposition.pdf',            'Traffic Case #6 [2013 - unknown]',                        '',              '2025-01-24'),
    ('section', 'Section VI', 'Miscellaneous'),
    (46, 'College_Card_Final_Statement_Aug-Sept_2020.pdf',              'Paid in Full/Settlement 1',                               '',              '2025-02-05'),
    (47, 'Birth_Certificate_DGN.pdf',                                   'Documentation of Citizenship',                            '1991-05-31',    '2025-01-22'),
]

MONTHS = ['January','February','March','April','May','June',
          'July','August','September','October','November','December']

def fmt_date(d):
    if not d or d in ('n/a','na',''):
        return u'\u2014'
    if d.startswith('Class'):
        return d
    try:
        parts = d.split('-')
        if len(parts) == 3:
            return f"{MONTHS[int(parts[1])-1]} {int(parts[2])}, {parts[0]}"
    except:
        pass
    return d

def dots_between(c, x1, x2, y, font="Times-Roman", size=9):
    gap = x2 - x1
    if gap <= 2: return
    d = ""
    while c.stringWidth(d + ".", font, size) < gap:
        d += "."
    c.setFont(font, size)
    c.drawString(x1, y, d)

doc_page_counts = {}
for e in STRUCTURE:
    if e[0] == 'section': continue
    num, fname = e[0], e[1]
    try:
        doc_page_counts[num] = len(PdfReader(os.path.join(repo, fname)).pages)
    except Exception as ex:
        print(f"ERROR reading {fname}: {ex}")
        doc_page_counts[num] = 1

def compute_layout(structure, doc_page_counts, toc_pages=1):
    layout = {}
    current = 1 + toc_pages
    si = 0
    for e in structure:
        if e[0] == 'section':
            layout[f's{si}'] = current
            si += 1; current += 1
        else:
            layout[e[0]] = current
            current += doc_page_counts.get(e[0], 1)
    return layout

def make_cover():
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=letter)
    ys = h - 3.2*inch
    c.setFont("Times-Roman", 10)
    c.drawCentredString(w/2, ys,      "BEFORE THE COMMITTEE ON CHARACTER AND FITNESS")
    c.drawCentredString(w/2, ys - 15, "OF THE SUPREME COURT OF ARIZONA")
    lx = 1.0*inch; rcx = 4.4*inch; bt = ys - 50; lh = 18
    c.setFont("Times-Roman", 11)
    c.drawString(lx, bt, "In the Matter of the Application of")
    ind = lx + c.stringWidth("In the ", "Times-Roman", 11)
    c.setFont("Times-Bold", 11)
    c.drawString(ind, bt - lh, "DAVID GARIBOTTO NIMER")
    c.setFont("Times-Roman", 11)
    c.drawString(lx, bt - lh*2, "To Be Admitted to the Practice of Law")
    lt = bt + 10; lb = bt - lh*2 - 12
    c.setLineWidth(0.75)
    c.line(rcx - 0.15*inch, lt, rcx - 0.15*inch, lb)
    c.line(lx, lb, rcx - 0.15*inch, lb)
    c.setFont("Times-BoldItalic", 10)
    rx = rcx + 0.1*inch
    c.drawString(rx, bt,      "Application (Amended) and")
    c.drawString(rx, bt - lh, "Supporting Documents")
    c.save(); buf.seek(0); return buf

def make_divider(sec_num, sec_title):
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=letter)
    base_y = h * (2.0/3.0)
    c.setFont("Times-Bold", 14)
    c.drawCentredString(w/2, base_y + 24, sec_num)
    c.setFont("Times-Roman", 13)
    c.drawCentredString(w/2, base_y, sec_title)
    c.setLineWidth(0.5)
    c.line(1.0*inch, base_y - 16, w - 1.0*inch, base_y - 16)
    c.save(); buf.seek(0); return buf

def make_toc(structure, layout, toc_page_offset=1):
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=letter)
    link_records = []
    toc_local = 0
    ROW_H = 0.185*inch
    y = h - 1.0*inch

    # Column positions — evenly spaced
    NUM_X    = ML
    NAME_X   = ML + 0.32*inch
    NAME_END = ML + 3.0*inch
    DATE_C_X = ML + 3.3*inch   # Created — shifted right
    DATE_U_X = ML + 4.45*inch  # Uploaded — shifted right, evenly spaced
    PAGE_X   = MR

    c.setFont("Times-Bold", 13)
    c.drawCentredString(w/2, y, "TABLE OF CONTENTS")
    y -= 0.35*inch

    c.setFont("Times-Bold", 9)
    c.drawString(NUM_X,    y, "#")
    c.drawString(NAME_X,   y, "Document Name")
    c.drawString(DATE_C_X, y, "Created")
    c.drawString(DATE_U_X, y, "Uploaded")
    c.drawRightString(PAGE_X, y, "Page")
    y -= 0.04*inch
    c.setLineWidth(0.5); c.line(ML, y, MR, y)
    y -= ROW_H

    si = 0
    for e in structure:
        if y < 0.75*inch:
            c.showPage(); toc_local += 1; y = h - 0.75*inch

        if e[0] == 'section':
            target = layout.get(f's{si}', 0); si += 1
            y -= 0.04*inch
            c.setFont("Times-Bold", 9)
            c.setFillColorRGB(0.15, 0.15, 0.45)
            label = f"{e[1]} \u2014 {e[2]}"
            c.drawString(NAME_X, y, label)
            # dots from section label to page number
            lw = c.stringWidth(label, "Times-Bold", 9)
            dots_between(c, NAME_X + lw + 4, PAGE_X - c.stringWidth(str(target+1), "Times-Roman", 9) - 4, y, "Times-Bold", 9)
            c.setFillColorRGB(0.15, 0.15, 0.45)
            c.drawRightString(PAGE_X, y, str(target + 1))
            c.setFillColorRGB(0,0,0)
            link_records.append((toc_page_offset + toc_local, (ML, y-2, MR, y+10), target))
            y -= ROW_H
        else:
            num, fname, name, created, uploaded = e
            target = layout.get(num, 0)
            c.setFont("Times-Roman", 9)
            c.drawString(NUM_X, y, str(num))

            dn = name
            while c.stringWidth(dn, "Times-Roman", 9) > (NAME_END - NAME_X) and len(dn) > 5:
                dn = dn[:-1]
            if dn != name: dn = dn[:-3] + "..."
            c.drawString(NAME_X, y, dn)

            dc = fmt_date(created)
            du = fmt_date(uploaded)
            pg_str = str(target + 1)

            c.drawString(DATE_C_X, y, dc)
            # dots: name end -> Created
            dots_between(c, NAME_X + c.stringWidth(dn, "Times-Roman", 9) + 3, DATE_C_X - 3, y)
            # dots: Created end -> Uploaded
            dots_between(c, DATE_C_X + c.stringWidth(dc, "Times-Roman", 9) + 3, DATE_U_X - 3, y)
            c.drawString(DATE_U_X, y, du)
            # dots: Uploaded end -> Page
            dots_between(c, DATE_U_X + c.stringWidth(du, "Times-Roman", 9) + 3, PAGE_X - c.stringWidth(pg_str, "Times-Roman", 9) - 3, y)
            c.drawRightString(PAGE_X, y, pg_str)

            link_records.append((toc_page_offset + toc_local, (ML, y-2, MR, y+10), target))
            y -= ROW_H

    c.save(); buf.seek(0)
    return buf, link_records

# Two-pass
layout = compute_layout(STRUCTURE, doc_page_counts, toc_pages=1)
toc_buf, _ = make_toc(STRUCTURE, layout, 1)
actual_toc_pages = len(PdfReader(toc_buf).pages)
print(f"TOC pages: {actual_toc_pages}")
layout = compute_layout(STRUCTURE, doc_page_counts, toc_pages=actual_toc_pages)
toc_buf, link_records = make_toc(STRUCTURE, layout, 1)

writer = PdfWriter()
for pg in PdfReader(make_cover()).pages: writer.add_page(pg)
toc_buf.seek(0)
for pg in PdfReader(toc_buf).pages: writer.add_page(pg)

si = 0
for e in STRUCTURE:
    if e[0] == 'section':
        for pg in PdfReader(make_divider(e[1], e[2])).pages: writer.add_page(pg)
        si += 1
    else:
        num, fname = e[0], e[1]
        path = os.path.join(repo, fname)
        try:
            r = PdfReader(path)
            for pg in r.pages: writer.add_page(pg)
            print(f"  OK [{num:2d}] {fname} ({len(r.pages)}p)")
        except Exception as ex:
            print(f"  SKIP [{num}] {fname}: {ex}")

total = len(writer.pages)
print(f"Total pages: {total}")

# Links — fix zoom by specifying explicit zoom=0 (inherit current zoom)
try:
    from pypdf.generic import (ArrayObject, FloatObject, NameObject,
                                NumberObject, DictionaryObject)
    for (toc_pg, rect, target_pg) in link_records:
        if toc_pg >= total or target_pg >= total: continue
        # Build explicit XYZ destination: page, left=0, top=page_height, zoom=0 (no change)
        page_obj = writer.pages[target_pg]
        dest = ArrayObject([
            page_obj.indirect_reference,
            NameObject("/XYZ"),
            FloatObject(0),
            FloatObject(float(page_obj.mediabox[3])),
            FloatObject(0),  # zoom=0 means keep current zoom
        ])
        annot = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Link"),
            NameObject("/Rect"): ArrayObject([
                FloatObject(rect[0]), FloatObject(rect[1]),
                FloatObject(rect[2]), FloatObject(rect[3])
            ]),
            NameObject("/Border"): ArrayObject([NumberObject(0), NumberObject(0), NumberObject(0)]),
            NameObject("/Dest"): dest,
        })
        writer.add_annotation(page_number=toc_pg, annotation=annot)
    print("Links OK (zoom preserved)")
except Exception as ex:
    print(f"Links error: {ex}")

# Bookmarks
si = 0
section_parents = {}
for e in STRUCTURE:
    if e[0] == 'section':
        pg = layout.get(f's{si}', 0)
        if pg < total:
            section_parents[si] = writer.add_outline_item(f"{e[1]} — {e[2]}", pg)
        si += 1
    else:
        num = e[0]; pg = layout.get(num, 0)
        parent_si = max([i for i in range(si) if layout.get(f's{i}', 999) <= pg], default=0)
        parent = section_parents.get(parent_si)
        if pg < total:
            writer.add_outline_item(f"{num}. {e[2]}", pg, parent=parent)

out = "/home/ubuntu/AZ_Bar_Merged.pdf"
with open(out, "wb") as f:
    writer.write(f)
size_mb = os.path.getsize(out) / 1024 / 1024
print(f"\nDONE: {out} ({size_mb:.1f} MB, {total} pages)")
