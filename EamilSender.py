import smtplib

SEND_EMAIL_EXCEPTIONS = (smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError,
                         smtplib.SMTPException, smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused)


class EmailSender:
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






