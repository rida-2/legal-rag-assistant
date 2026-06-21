from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(text):

    doc = SimpleDocTemplate(
        "generated_reports/legal_memo.pdf"
    )

    styles = getSampleStyleSheet()

    story = []

    for paragraph in text.split("\n"):

        story.append(
            Paragraph(paragraph, styles["Normal"])
        )

        story.append(Spacer(1, 12))

    doc.build(story)

    return "generated_reports/legal_memo.pdf"