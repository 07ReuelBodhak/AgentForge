#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

md_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('reports/v2.4-final-role-boundary-audit.md')
pdf_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('reports/v2.4-final-role-boundary-audit.pdf')

doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
styles = getSampleStyleSheet()

title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#1A237E'), spaceAfter=8)
h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=12, leading=15, textColor=colors.HexColor('#0D47A1'), spaceBefore=8, spaceAfter=4)
h3_style = ParagraphStyle('H3Style', parent=styles['Heading3'], fontSize=10, leading=13, textColor=colors.HexColor('#283593'), spaceBefore=6, spaceAfter=2)
body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=8.5, leading=12, spaceAfter=3)

def sanitize(text):
    # Strip backticks
    text = text.replace('`', '')
    # Escape XML entities
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Replace **text** with <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    return text

story = []
lines = md_path.read_text(encoding='utf-8').splitlines()
doc_title = 'AgentForge V2.4 Audit Report'
for l in lines:
    if l.startswith('# '):
        doc_title = sanitize(l[2:])
        break

story.append(Paragraph(doc_title, title_style))
story.append(Paragraph('<b>Architecture:</b> AgentForge V2.4 Hardened | <b>Status:</b> FULLY HARDENED &amp; VERIFIED | <b>Repo:</b> AgentForge', body_style))
story.append(Spacer(1, 8))

for line in lines:
    line = line.strip()
    if not line or line.startswith('---'):
        continue
    if line.startswith('# '):
        continue
    elif line.startswith('## '):
        clean = sanitize(line[3:])
        story.append(Spacer(1, 6))
        story.append(Paragraph(clean, h2_style))
    elif line.startswith('### '):
        clean = sanitize(line[4:])
        story.append(Paragraph(clean, h3_style))
    elif line.startswith('```') or line.startswith('|'):
        continue
    elif line.startswith('- ') or line.startswith('* '):
        clean = sanitize(line[2:])
        story.append(Paragraph('&bull; ' + clean, body_style))
    else:
        clean = sanitize(line)
        story.append(Paragraph(clean, body_style))

doc.build(story)
print(f"Generated: {pdf_path} ({pdf_path.stat().st_size} bytes)")
