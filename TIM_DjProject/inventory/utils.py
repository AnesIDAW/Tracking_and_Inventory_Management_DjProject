import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas

def generate_qr_image(data: str) -> ContentFile:
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue())

def generate_ticket_pdf(product) -> ContentFile:
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, "Delivery Ticket")

    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Product: {product.name}")
    p.drawString(100, 730, f"Method: {product.identification_method}")
    
    if product.identification_method == "QR":
        p.drawString(100, 710, f"QR Code ID: {product.id}")
    else:
        p.drawString(100, 710, f"RFID Tag: {product.rfid_tag}")

    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, 690, "Please attach this ticket to the product package.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return ContentFile(buffer.read())
