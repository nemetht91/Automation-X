from EamilSender import APIEmailSender
from forms import ContactForm
from settings import EMAIL_DOMAIN, EMAIL_API_KEY, SENDER, ENQUIRY_RECEIVER


class NotifierManger:
    def __init__(self):
        self.email_sender = APIEmailSender(domain_name=EMAIL_DOMAIN, api_key=EMAIL_API_KEY, sender=SENDER)

    def send_email(self, form: ContactForm):
        subject, letter = self.create_api_email_message(form)
        return self.email_sender.send_email(ENQUIRY_RECEIVER, subject, letter)

    @staticmethod
    def create_api_email_message(form: ContactForm):
        subject = f"New enquiry: {form.subject}"
        letter = f"Firstname: {form.firstname}\n" \
                 f"Lastname: {form.lastname}\n" \
                 f"Email: {form.email}\n" \
                 f"Phone number: {form.phone}\n" \
                 f"Company: {form.company}\n" \
                 f"\n{form.message}"

        return subject, letter

    @staticmethod
    def create_smtp_email_message(form: ContactForm):
        subject = f"New enquiry: {form.subject}"
        letter = f"Firstname: {form.firstname}\n" \
                 f"Lastname: {form.lastname}\n" \
                 f"Email: {form.email}\n" \
                 f"Phone number: {form.phone}\n" \
                 f"Company: {form.company}\n" \
                 f"\n{form.message}"
        email_message = f"Subject:{subject}\n\n{letter}"
        return email_message.encode('ascii', 'ignore').decode('ascii')