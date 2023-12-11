import smtplib
import requests
import mailtrap as mt
from settings import *

SEND_EMAIL_EXCEPTIONS = (smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError,
                         smtplib.SMTPException, smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused)


class MailtrapEmailSender:
    def __init__(self, domain: str, token: str):
        self.domain = domain
        self.token = token

    def send_enquiry(self, sender_name, receiver_address, subject, message, category):
        mail = self.__create_mail(sender_name, receiver_address, subject, message, category)
        return self.__send_mail(mail)

    def send_auto_reply(self, sender_name: str, receiver_address: str, template_uuid: str,
                        template_variables: dict):
        mail = self.__create_template_mail(sender_name, receiver_address, template_uuid, template_variables)
        return self.__send_mail(mail)

    def __send_mail(self, mail):
        client = mt.MailtrapClient(token=self.token)
        try:
            client.send(mail)
            return True
        except (mt.exceptions.MailtrapError, mt.exceptions.APIError, mt.exceptions.AuthorizationError) as e:
            print(e)
            return False

    def __create_mail(self, sender_name: str, receiver_address: str, subject: str, message: str, category: str):
        return mt.Mail(
            sender=mt.Address(email=f"{sender_name.lower()}@{self.domain}", name=sender_name),
            to=[mt.Address(email=receiver_address)],
            subject=subject,
            text=message,
            category=category,
        )

    def __create_template_mail(self, sender_name: str, receiver_address: str, template_uuid: str,
                               template_variables: dict):
        return mt.MailFromTemplate(
            sender=mt.Address(email=f"{sender_name.lower()}@{self.domain}", name=sender_name),
            to=[mt.Address(email=receiver_address)],
            template_uuid=template_uuid,
            template_variables=template_variables
        )


class MailGunEmailSender:
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
