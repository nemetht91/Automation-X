from EamilSender import EmailSender
from forms import ContactForm
from settings import SMTP_SERVER, SMTP_EMAIL, SMTP_PASSWORD


class NotifierManger:
    def __init__(self):
        self.email_sender = EmailSender(server=SMTP_SERVER, email=SMTP_EMAIL, password=SMTP_PASSWORD)

    def send_email(self, form: ContactForm):
        message = self.create_email_message(form)
        return self.email_sender.send_email(form.email, message)

    @staticmethod
    def create_email_message(form: ContactForm):
        subject = f"New enquiry: {form.subject}"
        letter = f"Firstname: {form.firstname}\n" \
                 f"Lastname: {form.lastname}\n" \
                 f"Company: {form.company}\n" \
                 f"\n{form.message}"
        email_message = f"Subject:{subject}\n\n{letter}"
        return email_message.encode('ascii', 'ignore').decode('ascii')