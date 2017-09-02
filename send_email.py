"""Send email notification"""
import os
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail


def send_email(receiver, present, past):
    """main method"""

    sg_client = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("WizzairPriceChange@konrad.com")
    to_email = Email(receiver)
    subject = "WizzAir ABZ -> GDN Alert"
    message = "Changed from: " + past + " GBP to: " + present + " GBP."
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    sg_client.client.mail.send.post(request_body=mail.get())
