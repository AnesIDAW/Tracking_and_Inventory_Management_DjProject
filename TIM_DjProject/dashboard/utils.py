from django.core.mail import send_mail
from twilio.rest import Client

def send_delivery_notification(product):
    user = product.client
    subject = f"Your product '{product.name}' was delivered"
    message = f"Hello {user.first_name},\n\nYour product '{product.name}' was delivered on {product.last_scanned_time}."
    recipient_list = [product.receiver_email]

    send_mail(
        subject,
        message,
        'naimianes312@gmail.com',
        recipient_list,
        fail_silently=False,
    )

def send_sms_notification(user, product):
    client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")
    message = client.messages.create(
        to=user.phone_number,
        from_="Twilio_Number",
        body=f"Hi {user.first_name}, your product '{product.name}' has been delivered!"
    )