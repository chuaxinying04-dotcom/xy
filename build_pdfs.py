"""Builds the slide deck (16:9 PDF). Edit the DATA block, run `python build_pdfs.py`,
then commit portfolio/Xin-Ying-Chua-Profile-Slides.pdf.
The CV download on the site is your own resume PDF (portfolio/Chua-Xin-Ying-Resume.pdf).
Font: Helvetica (built in). For Roboto, register Roboto TTFs with pdfmetrics and set FONT / BOLD."""
import os
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

FONT, BOLD = "Helvetica", "Helvetica-Bold"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio")
BLACK, GREY, LIGHT, SOFT = colors.HexColor("#111111"), colors.HexColor("#555555"), colors.HexColor("#d4d4d4"), colors.HexColor("#bbbbbb")

# ------------------------------- DATA -------------------------------
NAME = "Xin Ying Chua"
TITLE = "Accounting and Finance Graduate"
EMAIL = "chuaxinying2@gmail.com"
LINKEDIN = "www.linkedin.com/in/xin-ying-chua-964332140"
LINKEDIN_URL = "https://www.linkedin.com/in/xin-ying-chua-964332140"
SUMMARY = ("Sunway University graduate with a keen interest in financial markets and capital growth. "
           "Experience across treasury, insurance reporting and audit.")
FIGURES = [("3.69", "CGPA, Sunway University"), ("4", "finance placements"), ("10", "As in SPM"), ("200+", "camp participants led")]
JOBS = [
    ("FSTEP, Global Market", "United Overseas Bank (Malaysia)", "July 2026 to present",
     ["Execute treasury transactions and give hedging advice to clients",
      "Work with branches and partners to drive treasury product sales",
      "Monitor global markets, economic indicators and treasury trends"]),
    ("Intern, Business Management Unit, Global Market", "OCBC Bank (Malaysia)", "Oct 2025 to Feb 2026",
     ["Analysed segment volume trends and transaction counts for heads of departments",
      "Documented structured product meetings with Market Risk, Finance and Treasury Operations",
      "Prepared daily market recaps; helped build an Excel VBA automation macro"]),
    ("Intern, IFRS 17 Reporting, Finance", "Prudential BSN Takaful", "Jan 2025 to Apr 2025",
     ["Maintained the Power BI finance dashboard with daily sales and case data",
      "Mapped data item codes for the Insurance and Takaful System Redevelopment project",
      "Used Pivot Tables, SUMIFS, XLOOKUP and VLOOKUP to speed up reporting"]),
    ("Assurance Intern, Financial Services Line (Insurance)", "PwC Malaysia", "Jan 2024 to Mar 2024",
     ["Reviewed client financial statements and operating procedures",
      "Executed evidence gathering activities to support audit opinions",
      "Tested samples and verified draft statements by casting and cross-referencing"]),
]
EDU = [("BSc (Hons) in Accounting and Finance", "Sunway University", "2022 to 2025", "CGPA: 3.69"),
       ("Chong Hwa Independent High School, Kuala Lumpur", "", "2016 to 2021", "UEC 2021: 8As.  SPM 2020: 10As.")]
LEAD = [("Secretary and Treasurer, KPMG Ambassador 2024", "Sunway University. Supported KPMG Malaysia campus events and recruitment."),
        ("Financial Controller, Executive Committee 2023/2024", "Sunway Chinese Independent School Alumni. Managed and audited club accounts."),
        ("Head of Department, Secretary and Treasurer", "Sunway Ambassador Leadership Trek 2023. Liaised with 13 independent high schools."),
        ("Vice-Chairman and Camp Vice Leader, 2020 and 2021", "Chong Hwa Leadership Camp. Planned activities for 200+ participants.")]
SKILLS = ["Languages: English, Mandarin, Malay", "Computing: Microsoft Office 365, Canva, Power BI",
          "Excel: Pivot Tables, SUMIFS, XLOOKUP, VLOOKUP", "Basic SQL Accounting software",
          "Adaptability, problem-solving, proactivity"]
HONOURS = ["Sunway Business School Book Prize Award: Personal Financial Planning and International Financial Management",
           "Dean's List Award", "Jeffrey Cheah Entrance Scholarship",
           "Overall 4th Position in Senior Middle Three Arts 2021",
           "Outstanding Service Award for Extra-Curricular Activities 2021"]
# --------------------------------------------------------------------

W, H = 338.67*mm, 190.5*mm  # 16:9
M = 25*mm
c = canvas.Canvas(os.path.join(OUT, "Xin-Ying-Chua-Profile-Slides.pdf"), pagesize=(W, H))
c.setTitle(f"{NAME} | Profile"); c.setAuthor(NAME)
count = [0]


def wrap(text, font, size, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if c.stringWidth(t, font, size) > width and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]


def para(text, x, y, font, size, width, lead, color=BLACK):
    c.setFillColor(color); c.setFont(font, size)
    for l in wrap(text, font, size, width):
        c.drawString(x, y, l); y -= lead
    return y


def slide(dark=False, title=None):
    if count[0]: c.showPage()
    count[0] += 1
    c.setFillColor(BLACK if dark else colors.white); c.rect(0, 0, W, H, stroke=0, fill=1)
    if title:
        c.setFillColor(BLACK); c.setFont(BOLD, 30); c.drawString(M, H - 38*mm, title)
        c.setStrokeColor(BLACK); c.setLineWidth(2); c.line(M, H - 44*mm, M + 22*mm, H - 44*mm)
        c.setFillColor(GREY); c.setFont(FONT, 11); c.drawString(M, 12*mm, NAME)
        c.drawRightString(W - M, 12*mm, str(count[0]))


TOP = H - 60*mm

# Title
slide(dark=True)
c.setFillColor(colors.white); c.setFont(BOLD, 54); c.drawString(M, H/2 + 4*mm, NAME)
c.setFillColor(SOFT); c.setFont(FONT, 22); c.drawString(M, H/2 - 10*mm, TITLE)
c.setFont(FONT, 13); c.drawString(M, 20*mm, f"{EMAIL}   |   {LINKEDIN}")

# Profile
slide(title="Profile")
para(SUMMARY, M, TOP, FONT, 18, W - 2*M, 9*mm)
cw = (W - 2*M) / len(FIGURES)
for i, (v, l) in enumerate(FIGURES):
    x = M + i*cw
    c.setStrokeColor(BLACK); c.setLineWidth(1); c.line(x, 62*mm, x + cw - 8*mm, 62*mm)
    c.setFillColor(BLACK); c.setFont(BOLD, 44); c.drawString(x, 40*mm, v)
    c.setFillColor(GREY); c.setFont(FONT, 13); c.drawString(x, 31*mm, l)

# Experience, two roles per slide
for i in range(0, len(JOBS), 2):
    slide(title="Experience" if i == 0 else "Experience (continued)")
    y = TOP
    for role, org, when, bl in JOBS[i:i+2]:
        c.setFillColor(BLACK); c.setFont(BOLD, 17); c.drawString(M, y, role)
        c.setFillColor(GREY); c.setFont(FONT, 13); c.drawRightString(W - M, y, when)
        y -= 6.5*mm
        c.setFont(FONT, 13); c.drawString(M, y, org); y -= 8*mm
        for b in bl:
            y = para(b, M + 5*mm, y, FONT, 13.5, W - 2*M - 5*mm, 6.2*mm)
            c.setFillColor(BLACK); c.circle(M + 1.5*mm, y + 7.2*mm, 0.8*mm, stroke=0, fill=1)
        y -= 9*mm

# Education
slide(title="Education")
y = TOP
for name, org, when, note in EDU:
    c.setFillColor(BLACK); c.setFont(BOLD, 20); c.drawString(M, y, name)
    c.setFillColor(GREY); c.setFont(FONT, 14); c.drawRightString(W - M, y, when)
    y -= 8*mm
    if org: c.setFillColor(BLACK); c.setFont(FONT, 16); c.drawString(M, y, org); y -= 8*mm
    c.setFillColor(BLACK); c.setFont(FONT, 16); c.drawString(M, y, note); y -= 22*mm

# Leadership
slide(title="Leadership and activities")
y = TOP
for head, line in LEAD:
    c.setStrokeColor(LIGHT); c.setLineWidth(0.7); c.line(M, y + 7*mm, W - M, y + 7*mm)
    c.setFillColor(BLACK); c.setFont(BOLD, 16); c.drawString(M, y - 2*mm, head)
    c.setFillColor(GREY); c.setFont(FONT, 13.5); c.drawString(M, y - 9*mm, line)
    y -= 24*mm

# Skills and honours
slide(title="Skills and honours")
half = (W - 2*M) / 2 - 8*mm
c.setFillColor(BLACK); c.setFont(BOLD, 16); c.drawString(M, TOP, "Skills"); c.drawString(M + half + 16*mm, TOP, "Honours")
y = TOP - 10*mm
for s in SKILLS: y = para(s, M, y, FONT, 14, half, 6.2*mm) - 4*mm
y = TOP - 10*mm
for h in HONOURS: y = para(h, M + half + 16*mm, y, FONT, 14, half, 6.2*mm) - 4*mm

# Contact
slide(dark=True)
c.setFillColor(colors.white); c.setFont(BOLD, 40); c.drawString(M, H/2 + 12*mm, "Let's talk")
c.setFont(FONT, 18); c.setFillColor(SOFT)
c.drawString(M, H/2 - 2*mm, EMAIL); c.drawString(M, H/2 - 12*mm, LINKEDIN)
c.linkURL(LINKEDIN_URL, (M, H/2 - 16*mm, M + 130*mm, H/2 - 6*mm), relative=0)
c.save()
print("done")
