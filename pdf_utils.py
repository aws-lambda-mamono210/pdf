from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io

def create_pdf_with_text(text, output_path):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.drawString(100, 100, text)
    c.showPage()
    c.save()
    packet.seek(0)

    new_pdf = PdfReader(packet)
    with open(output_path, "wb") as f:
        pdf_writer = PdfWriter()
        pdf_writer.add_page(new_pdf.pages[0])
        pdf_writer.write(f)
