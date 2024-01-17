from os import environ

# Email API Server
EMAIL_DOMAIN = environ.get("EMAIL_DOMAIN")
EMAIL_API_KEY = environ.get("EMAIL_API_KEY")
SENDER = environ.get("SENDER")

# Mailtrap Email Server
MAILTRAP_DOMAIN = environ.get("MAILTRAP_DOMAIN")
MAILTRAP_SENDER = environ.get("MAILTRAP_SENDER")
MAILTRAP_TOKEN = environ.get("MAILTRAP_TOKEN")
MAILTRAP_NO_REPLY_UUID = environ.get("MAILTRAP_NO_REPLY_UUID")

# Enquiry handler
ENQUIRY_RECEIVER = environ.get("ENQUIRY_RECEIVER")

# Admin user
ADMIN_USERNAME = environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD")