from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
from datetime import datetime

def generate_ticket_pdf(product):
    buffer = BytesIO()
    width, height = A5
    c = canvas.Canvas(buffer, pagesize=A5)

    # Enhanced margins and spacing
    margin_outer = 15 * mm
    margin_inner = 8 * mm
    border_width = 1.5
    
    # Color scheme
    primary_color = colors.Color(0.2, 0.3, 0.5)  # Dark blue
    secondary_color = colors.Color(0.9, 0.9, 0.9)  # Light gray
    text_color = colors.Color(0.2, 0.2, 0.2)  # Dark gray

    # Draw outer border with rounded effect
    c.setLineWidth(border_width)
    c.setStrokeColor(primary_color)
    c.rect(margin_outer, margin_outer, width - 2 * margin_outer, height - 2 * margin_outer)

    # Header section with background
    header_height = 35 * mm
    c.setFillColor(primary_color)
    c.rect(margin_outer + border_width, height - margin_outer - header_height, 
           width - 2 * margin_outer - 2 * border_width, header_height, fill=1, stroke=0)

    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    title_y = height - margin_outer - 20 * mm
    c.drawCentredString(width / 2, title_y, "DELIVERY TICKET")
    
    # Subtitle
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, title_y - 15, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Content area positioning
    content_start_y = height - margin_outer - header_height - 10 * mm
    left_column_x = margin_outer + margin_inner
    right_column_x = width / 2 + 5 * mm
    line_height = 16
    section_spacing = 8

    # Helper function to draw labeled fields
    def draw_field(x, y, label, value, font_size=11, label_width=None):
        c.setFillColor(text_color)
        c.setFont("Helvetica-Bold", font_size)
        c.drawString(x, y, f"{label}:")
        
        # Calculate value position
        if label_width:
            value_x = x + label_width
        else:
            label_text_width = c.stringWidth(f"{label}:", "Helvetica-Bold", font_size)
            value_x = x + label_text_width + 5
        
        c.setFont("Helvetica", font_size)
        c.drawString(value_x, y, str(value))
        return y - line_height

    # Draw sections with better organization
    y_pos = content_start_y

    # Section 1: Product Information
    c.setFillColor(secondary_color)
    section_bg_height = 4 * line_height + 10
    c.rect(left_column_x - 3, y_pos - section_bg_height + line_height, 
           width - 2 * margin_outer - 2 * margin_inner + 6, section_bg_height, fill=1, stroke=0)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(left_column_x, y_pos, "PRODUCT DETAILS")
    y_pos -= line_height + section_spacing

    y_pos = draw_field(left_column_x, y_pos, "Product Name", product.name, label_width=80)
    y_pos = draw_field(left_column_x, y_pos, "Ticket Number", product.ticket, label_width=80)
    y_pos = draw_field(left_column_x, y_pos, "Status", product.status.title(), label_width=80)
    y_pos -= section_spacing

    # Section 2: Client & Delivery Information
    c.setFillColor(secondary_color)
    section_bg_height = 5 * line_height + 10
    c.rect(left_column_x - 3, y_pos - section_bg_height + line_height, 
           width - 2 * margin_outer - 2 * margin_inner + 6, section_bg_height, fill=1, stroke=0)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(left_column_x, y_pos, "DELIVERY INFORMATION")
    y_pos -= line_height + section_spacing

    y_pos = draw_field(left_column_x, y_pos, "Client", product.client.username, label_width=80)
    y_pos = draw_field(left_column_x, y_pos, "Warehouse", product.warehouse_location or "N/A", label_width=80)
    
    if product.vehicle:
        y_pos = draw_field(left_column_x, y_pos, "Vehicle Plate", product.vehicle.plate_number, label_width=80)
    
    y_pos = draw_field(left_column_x, y_pos, "Receiver", product.receiver_name or "N/A", label_width=80)
    y_pos -= section_spacing

    # Section 3: Contact Information
    c.setFillColor(secondary_color)
    section_bg_height = 3 * line_height + 10
    c.rect(left_column_x - 3, y_pos - section_bg_height + line_height, 
           width - 2 * margin_outer - 2 * margin_inner + 6, section_bg_height, fill=1, stroke=0)
    
    c.setFillColor(primary_color)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(left_column_x, y_pos, "CONTACT DETAILS")
    y_pos -= line_height + section_spacing

    y_pos = draw_field(left_column_x, y_pos, "Email", product.receiver_email or "N/A", label_width=80)
    y_pos = draw_field(left_column_x, y_pos, "Phone", product.receiver_phone_number or "N/A", label_width=80)

    # QR Code section (positioned on the right side)
    if product.identification_method == "qr code" and product.qr_code:
        qr = qrcode.QRCode(
            version=1,
            box_size=8,
            border=2,
        )
        qr.add_data(product.qr_code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        qr_buffer = BytesIO()
        img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        qr_image = ImageReader(qr_buffer)

        # QR code positioning
        qr_size = 60
        qr_x = width - margin_outer - margin_inner - qr_size
        qr_y = margin_outer + 40
        
        # QR code background
        c.setFillColor(colors.white)
        c.setStrokeColor(primary_color)
        c.setLineWidth(1)
        padding = 5
        c.rect(qr_x - padding, qr_y - padding, qr_size + 2*padding, qr_size + 2*padding, fill=1, stroke=1)
        
        # Draw QR code
        c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)
        
        # QR code label
        c.setFillColor(text_color)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(qr_x + qr_size/2, qr_y - 15, "Scan for Details")

    # Footer section
    footer_y = margin_outer + 10
    c.setStrokeColor(primary_color)
    c.setLineWidth(0.5)
    c.line(margin_outer + margin_inner, footer_y + 15, 
           width - margin_outer - margin_inner, footer_y + 15)
    
    c.setFillColor(text_color)
    c.setFont("Helvetica", 9)
    c.drawString(margin_outer + margin_inner, footer_y, 
                 "This is an automatically generated delivery ticket. Please keep for your records.")
    
    # Page number (if needed for multi-page documents)
    c.drawRightString(width - margin_outer - margin_inner, footer_y, "Page 1")

    c.showPage()
    c.save()
    buffer.seek(0)

    file_name = f"{product.name}_delivery_ticket_{product.ticket}_{datetime.now().strftime('%Y%m%d')}.pdf"
    return ContentFile(buffer.getvalue(), name=file_name)