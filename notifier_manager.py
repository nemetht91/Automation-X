from EamilSender import MailtrapEmailSender
from forms import ContactForm
from settings import *


class NotifierManger:
    def __init__(self):
        self.email_sender = MailtrapEmailSender(domain=MAILTRAP_DOMAIN, token=MAILTRAP_TOKEN)

    def send_enquiry(self, form: ContactForm):
        subject, letter = self.create_api_email_message(form)
        return self.email_sender.send_enquiry(MAILTRAP_SENDER, ENQUIRY_RECEIVER, subject, letter, category="Enquiry")

    def send_auto_reply(self, form: ContactForm):
        message = self.split_into_list(form.message)
        template_variables = {
            "first_name": form.firstname,
            "last_name": form.lastname,
            "enquiry": {
                "lines": message
            }
        }
        return self.email_sender.send_auto_reply("no-reply", form.email, MAILTRAP_NO_REPLY_UUID, template_variables)

    @staticmethod
    def split_into_list(text: str) -> []:
        return text.split("\n")

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