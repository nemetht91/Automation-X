from os import environ

# Email API Server
EMAIL_DOMAIN = environ.get("EMAIL_DOMAIN")
EMAIL_API_KEY = environ.get("EMAIL_API_KEY")
SENDER = environ.get("SENDER")

# Enquiry handler
ENQUIRY_RECEIVER = environ.get("ENQUIRY_RECEIVER")
