"""Builds the CV (A4) and the slide deck (16:9) as PDFs.
Edit the DATA block, run `python build_pdfs.py`, then commit the two PDFs.
Font: Helvetica (built in). To use Roboto, register Roboto-Regular.ttf and
Roboto-Bold.ttf with pdfmetrics.registerFont and set FONT / BOLD below."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfgen import canvas

FONT, BOLD = "Helvetica", "Helvetica-Bold"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio")
BLACK, GREY, LIGHT = colors.HexColor("#111111"), colors.HexColor("#555555"), colors.HexColor("#d4d4d4")

# ------------------------------- DATA -------------------------------
NAME = "Xin Ying Chua"
TITLE = "Financial Analyst"
EMAIL = "you@example.com"
LINKEDIN = "www.linkedin.com/in/xin-ying-chua-964332140"
LINKEDIN_URL = "https://www.linkedin.com/in/xin-ying-chua-964332140"
LOCATION = "Selangor, Malaysia"
SUMMARY = ("Financial analyst focused on forecasting, risk and foreign exchange. "
           "I build models that finance teams can trust and explain.")
JOBS = [
    ("Financial Analyst", "Company Name", "2024 to present",
     ["Own the monthly forecast and variance reporting for a RM 50m portfolio.",
      "Cut month-end close time by two days by automating reconciliations.",
      "Present results to senior management each quarter."]),
    ("Junior Analyst", "Company Name", "2022 to 2024",
     ["Prepared FX exposure reports across three currencies.",
      "Supported treasury with hedging analysis and risk limit monitoring."]),
]
EDU = [("BA Finance", "University Name", "2018 to 2022", "Graduated with honours. Thesis on interest rate risk in small banks.")]
SKILLS = [("Technical", "Financial modelling, forecasting, variance analysis, FX and risk management"),
          ("Tools", "Excel, SQL, Python, Power BI"),
          ("Languages", "English, Mandarin, Bahasa Malaysia")]
CERTS = ["Certification name, Issuer (year)", "Certification name, Issuer (year)"]
PROJECTS = [("FX Exposure Dashboard", "Tracks currency exposure by business unit and flags limit breaches.", "Excel, Power BI"),
            ("Cash Flow Forecast Model", "13-week rolling forecast with best, base and worst cases.", "Excel, Python"),
            ("Loan Portfolio Review", "Segments loans by credit quality and estimates expected losses.", "SQL, Tableau")]
FIGURES = [("4", "years in finance"), ("25+", "models built"), ("94%", "forecast accuracy"), ("120", "reports delivered")]
# --------------------------------------------------------------------


def build_cv(path):
    st = lambda n, **k: ParagraphStyle(n, fontName=k.pop("f", FONT), **k)
    name = st("n", fontSize=26, leading=30, f=BOLD, textColor=BLACK)
    sub = st("s", fontSize=12, leading=16, textColor=GREY)
    h = st("h", fontSize=10.5, leading=14, f=BOLD, textColor=BLACK, spaceBefore=11, spaceAfter=3)
    body = st("b", fontSize=9.5, leading=13.5, textColor=BLACK)
    role = st("r", fontSize=10.5, leading=14, f=BOLD, textColor=BLACK)
    meta = st("m", fontSize=9.5, leading=14, textColor=GREY, alignment=2)
    bullet = st("bl", fontSize=9.5, leading=13.5, leftIndent=11, bulletIndent=0)

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=17*mm, bottomMargin=15*mm, title=f"{NAME} CV", author=NAME)
    s = [Paragraph(NAME, name), Paragraph(TITLE, sub), Spacer(1, 3),
         Paragraph(f'{EMAIL} &nbsp;|&nbsp; {LOCATION} &nbsp;|&nbsp; '
                   f'<link href="{LINKEDIN_URL}" color="#111111"><u>{LINKEDIN}</u></link>', body),
         Spacer(1, 6), HRFlowable(width="100%", thickness=1.5, color=BLACK, spaceAfter=2)]

    def section(t):
        s.extend([Paragraph(t, h), HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=4)])

    def entry(left, right, lines=None, text=None):
        t = Table([[Paragraph(left, role), Paragraph(right, meta)]], colWidths=[120*mm, 50*mm])
        t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
        s.append(t)
        if text: s.append(Paragraph(text, body))
        for l in lines or []: s.append(Paragraph(l, bullet, bulletText="\u2022"))
        s.append(Spacer(1, 5))

    section("PROFILE"); s.append(Paragraph(SUMMARY, body))
    section("EXPERIENCE")
    for r, c, d, b in JOBS: entry(f"{r}, {c}", d, lines=b)
    section("PROJECTS")
    for p, d, t in PROJECTS: entry(p, t, text=d)
    section("EDUCATION")
    for e, u, d, t in EDU: entry(f"{e}, {u}", d, text=t)
    section("SKILLS")
    for k, v in SKILLS: s.append(Paragraph(f"<b>{k}:</b> {v}", body))
    section("CERTIFICATIONS")
    for c in CERTS: s.append(Paragraph(c, bullet, bulletText="\u2022"))
    doc.build(s)


def build_slides(path):
    W, H = 338.67*mm, 190.5*mm  # 16:9
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle(f"{NAME} | Profile"); c.setAuthor(NAME)
    M = 25*mm
    n = [0]

    def page(dark=False, title=None):
        if n[0]: c.showPage()
        n[0] += 1
        c.setFillColor(BLACK if dark else colors.white); c.rect(0, 0, W, H, stroke=0, fill=1)
        if title and not dark:
            c.setFillColor(BLACK); c.setFont(BOLD, 30); c.drawString(M, H - 38*mm, title)
            c.setStrokeColor(BLACK); c.setLineWidth(2); c.line(M, H - 44*mm, M + 22*mm, H - 44*mm)
            c.setFillColor(GREY); c.setFont(FONT, 11); c.drawString(M, 12*mm, NAME)
            c.drawRightString(W - M, 12*mm, str(n[0]))

    # 1 Title
    page(dark=True)
    c.setFillColor(colors.white); c.setFont(BOLD, 54); c.drawString(M, H/2 + 4*mm, NAME)
    c.setFillColor(colors.HexColor("#bbbbbb")); c.setFont(FONT, 22); c.drawString(M, H/2 - 10*mm, TITLE)
    c.setFont(FONT, 13); c.drawString(M, 20*mm, f"{EMAIL}   |   {LINKEDIN}")
    # 2 Profile + figures
    page(title="Profile")
    y = H - 62*mm
    c.setFillColor(BLACK); c.setFont(FONT, 17)
    words, line = SUMMARY.split(), ""
    for w in words:
        if c.stringWidth(line + " " + w, FONT, 17) > W - 2*M: c.drawString(M, y, line.strip()); y -= 9*mm; line = w
        else: line += " " + w
    c.drawString(M, y, line.strip())
    cw = (W - 2*M) / len(FIGURES)
    for i, (v, l) in enumerate(FIGURES):
        x = M + i*cw
        c.setStrokeColor(BLACK); c.setLineWidth(1); c.line(x, 62*mm, x + cw - 8*mm, 62*mm)
        c.setFillColor(BLACK); c.setFont(BOLD, 44); c.drawString(x, 40*mm, v)
        c.setFillColor(GREY); c.setFont(FONT, 13); c.drawString(x, 31*mm, l)
    # 3 Experience
    page(title="Experience")
    y = H - 62*mm
    for r, co, d, b in JOBS:
        c.setFillColor(BLACK); c.setFont(BOLD, 18); c.drawString(M, y, f"{r}, {co}")
        c.setFillColor(GREY); c.setFont(FONT, 13); c.drawRightString(W - M, y, d)
        y -= 8*mm
        c.setFillColor(BLACK); c.setFont(FONT, 14)
        for l in b[:3]: c.drawString(M + 4*mm, y, "\u2022  " + l); y -= 7*mm
        y -= 7*mm
    # 4 Projects
    page(title="Projects")
    y = H - 62*mm
    for p, d, t in PROJECTS:
        c.setStrokeColor(LIGHT); c.setLineWidth(0.7); c.line(M, y + 6*mm, W - M, y + 6*mm)
        c.setFillColor(BLACK); c.setFont(BOLD, 17); c.drawString(M, y - 3*mm, p)
        c.setFont(FONT, 13); c.setFillColor(GREY); c.drawString(M + 80*mm, y - 3*mm, d)
        c.drawRightString(W - M, y - 3*mm, t)
        y -= 20*mm
    # 5 Skills
    page(title="Skills and credentials")
    y = H - 62*mm
    for k, v in SKILLS:
        c.setFillColor(BLACK); c.setFont(BOLD, 15); c.drawString(M, y, k)
        c.setFont(FONT, 15); c.drawString(M + 50*mm, y, v); y -= 12*mm
    y -= 6*mm
    c.setFont(BOLD, 15); c.drawString(M, y, "Certifications")
    c.setFont(FONT, 15)
    for cert in CERTS: c.drawString(M + 50*mm, y, cert); y -= 9*mm
    # 6 Contact
    page(dark=True)
    c.setFillColor(colors.white); c.setFont(BOLD, 40); c.drawString(M, H/2 + 12*mm, "Let\u2019s talk")
    c.setFont(FONT, 18); c.setFillColor(colors.HexColor("#bbbbbb"))
    c.drawString(M, H/2 - 2*mm, EMAIL)
    c.drawString(M, H/2 - 12*mm, LINKEDIN)
    c.linkURL(LINKEDIN_URL, (M, H/2 - 16*mm, M + 130*mm, H/2 - 6*mm), relative=0)
    c.save()


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build_cv(os.path.join(OUT, "Xin-Ying-Chua-CV.pdf"))
    build_slides(os.path.join(OUT, "Xin-Ying-Chua-Profile-Slides.pdf"))
    print("done")
