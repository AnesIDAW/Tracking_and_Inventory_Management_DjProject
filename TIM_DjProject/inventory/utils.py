# utils.py
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


def generate_ticket_pdf(product):
    """Generate PDF ticket for a product, including a QR code if applicable."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Header Info
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Product Ticket")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Name: {product.name}")
    p.drawString(100, 780, f"Identification: {product.rfid_tag if product.identification_method == 'rfid' else "QR code"}")
    p.drawString(100, 760, f"Client: {product.client.username}")
    p.drawString(100, 720, f"Warehouse: {product.warehouse_location}")
    p.drawString(100, 700, f"Receiver: {product.receiver_name}")
    p.drawString(100, 680, f"Email: {product.receiver_email}")
    p.drawString(100, 660, f"Phone: {product.receiver_phone_number}")

    # Draw QR code if applicable
    if product.identification_method == "qr code" and product.qr_code:
        qr = qrcode.make(product.qr_code)
        qr_buffer = BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        qr_image = ImageReader(qr_buffer)
        p.drawImage(qr_image, 100, 500, width=150, height=150)

    p.showPage()
    p.save()
    buffer.seek(0)

    return ContentFile(buffer.read(), name=f"ticket_{product.name}.pdf")


