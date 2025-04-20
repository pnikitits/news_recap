from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from datetime import datetime
import logging


def generate_pdf(positive_headlines: list[str], negative_headlines: list[str], output_path: str, font_path: str = None):
    # Set up document
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)

    # Font
    if font_path:
        pdfmetrics.registerFont(TTFont('CustomFont', font_path))
        base_font = 'CustomFont'
    else:
        base_font = 'Times-Roman'

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Heading1Center', fontName=base_font, fontSize=20, alignment=1, spaceAfter=12))
    styles.add(ParagraphStyle(name='SubHeading', fontName=base_font, fontSize=16, spaceBefore=12, spaceAfter=6, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='Headline', fontName=base_font, fontSize=12, leading=15))
    styles.add(ParagraphStyle(name='Footer', fontName=base_font, fontSize=10, alignment=1, textColor=colors.grey))

    content = []

    # Title
    content.append(Paragraph("News Summary", styles['Heading1Center']))
    content.append(Spacer(1, 12))

    # Positive Headlines
    content.append(Paragraph("Ok News", styles['SubHeading']))
    for headline in positive_headlines:
        content.append(Paragraph("• " + headline, styles['Headline']))

    content.append(Spacer(1, 20))

    # Negative Headlines
    content.append(Paragraph("Depressing News", styles['SubHeading']))
    for headline in negative_headlines:
        content.append(Paragraph("• " + headline, styles['Headline']))

    # Add footer with date and optional page numbers
    def add_footer(canvas, doc):
        canvas.saveState()
        footer_text = f"Updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        canvas.setFont(base_font, 10)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        # canvas.drawCentredString(letter[0] / 2.0, 0.35 * inch, f"Page {doc.page}")
        canvas.restoreState()

    # Build PDF
    doc.build(content, onFirstPage=add_footer, onLaterPages=add_footer)

    logging.info(f"PDF created successfully at: {output_path}")
    return output_path




def sort_lines(headlines:list[str],
               responses:list[str]):
    positive_headlines = []
    negative_headlines = []
    for i in range(len(headlines)):
        if responses[i] == "ok":
            positive_headlines.append(headlines[i])
        elif responses[i] == "depressing":
            negative_headlines.append(headlines[i])
        else:
            raise ValueError(f"Unexpected response: {responses[i]}")
    return positive_headlines, negative_headlines