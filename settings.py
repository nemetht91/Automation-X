from os import environ

# Email API Server
EMAIL_DOMAIN = environ.get("EMAIL_DOMAIN")
EMAIL_API_KEY = environ.get("EMAIL_API_KEY")
SENDER = environ.get("SENDER")

# Mailtrap Email Server
MAILTRAP_EMAIL = environ.get("MAILTRAP_EMAIL")
MAILTRAP_SENDER = environ.get("MAILTRAP_SENDER")
MAILTRAP_TOKEN = environ.get("MAILTRAP_TOKEN")

# Enquiry handler
ENQUIRY_RECEIVER = environ.get("ENQUIRY_RECEIVER")
