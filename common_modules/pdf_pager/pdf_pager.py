from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io

def add_page_numbers(input_path, output_path, font_size=12, font_name="Helvetica"):
    # Load the existing PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_number in range(len(reader.pages)):
        # Get the existing page
        page = reader.pages[page_number]

        # Get the page size
        page_width = float(page.mediabox[2])
        page_height = float(page.mediabox[3])

        # Create a new PDF in memory to draw the page number
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # Set the font name and size
        c.setFont(font_name, font_size)

        # Draw the page number (the position can be adjusted as needed)
        c.drawCentredString(page_width / 2, 30, f"- {page_number + 1} -")
        c.save()

        # Get the new PDF data and merge it with the existing page
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])  # Already updated method name

        # Add the page to the new PDF
        writer.add_page(page)  # Updated method name here

    # Save the new PDF
    with open(output_path, "wb") as f:
        writer.write(f)
