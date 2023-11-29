import smtplib
import requests

SEND_EMAIL_EXCEPTIONS = (smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError,
                         smtplib.SMTPException, smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused)


class APIEmailSender:
    def __init__(self, domain_name, api_key, sender):
        self.domain_name = domain_name
        self.api_key = api_key
        self.sender = sender

    def send_email(self, receiver_address, subject, message):
        response = requests.post(
            f"https://api.mailgun.net/v3/{self.domain_name}/messages",
            auth=("api", self.api_key),
            data={"from": f"{self.sender}@{self.domain_name}",
                  "to": receiver_address,
                  "subject": subject,
                  "text": message})
        if response.status_code == 200:
            return True
        return False


class SMTPEmailSender:
    def __init__(self, server, email, password):
        self.server = server
        self.email = email
        self.password = password

    def send_email(self, receiver_address, message):
        """ Returns True successfully, False otherwise """
        try:
            with smtplib.SMTP(self.server) as connection:
                connection.starttls()
                connection.login(user=self.email, password=self.password)
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=receiver_address,
                    msg=message
                )
        except SEND_EMAIL_EXCEPTIONS as error_message:
            return False
        else:
            return True

