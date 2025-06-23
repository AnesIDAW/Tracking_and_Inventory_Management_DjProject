from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode

def generate_ticket_pdf(product):
    buffer = BytesIO()
    width, height = A5
    c = canvas.Canvas(buffer, pagesize=A5)

    margin = 12 * mm
    border_width = 2

    # Draw border
    c.setLineWidth(border_width)
    c.setStrokeColor(colors.black)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

    # Title
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - margin - 20, "Delivery Ticket")

    # Product information
    c.setFont("Helvetica", 14)
    y = height - margin - 50
    line_height = 22

    def draw_line(label, value):
        nonlocal y
        text = f"{label}: {value}"
        c.drawString(margin + 10, y, text)
        y -= line_height

    draw_line("Product Name", product.name)
    draw_line("Ticket Number", product.ticket)
    draw_line("Client", product.client.username)
    draw_line("Warehouse", product.warehouse_location or "N/A")
    draw_line("Status", product.status.title())
    if product.vehicle:
        draw_line("Vehicle Plate", product.vehicle.plate_number)
    draw_line("Receiver", product.receiver_name or "N/A")
    draw_line("Receiver Email", product.receiver_email or "N/A")
    draw_line("Receiver Phone", product.receiver_phone_number or "N/A")

    # Generate QR code if applicable
    if product.identification_method == "qr code" and product.qr_code:
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=2,
        )
        qr.add_data(product.qr_code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        qr_buffer = BytesIO()
        img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        qr_image = ImageReader(qr_buffer)

        c.drawImage(qr_image, width - 100, margin + 20, width=70, height=70)

    c.showPage()
    c.save()
    buffer.seek(0)

    file_name = f"ticket_{product.ticket}.pdf"
    return ContentFile(buffer.getvalue(), name=file_name)
