from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("certificate.pdf")
styles = getSampleStyleSheet()

story = []

story.append(Paragraph("<b>Python Learning Portal</b>", styles["Title"]))
story.append(Paragraph("Certificate of Completion", styles["Heading1"]))
story.append(Paragraph("This certificate is proudly awarded to", styles["Normal"]))
story.append(Paragraph("<b>Pavi</b>", styles["Heading2"]))
story.append(Paragraph("For successfully completing the Python Quiz.", styles["Normal"]))

doc.build(story)

print("Certificate Created Successfully!")