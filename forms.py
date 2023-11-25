class ContactForm:
    def __init__(self, form):
        self.firstname = form.get("firstname")
        self.lastname = form.get("lastname")
        self.email = form.get("email")
        self.company = form.get("company")
        self.phone = form.get("phone")
        self.subject = form.get("subject")
        self.message = form.get("message")

    def is_valid(self):
        return self.is_name_valid() and self.is_email_valid() and self.is_content_valid()

    def is_name_valid(self):
        if not self.firstname:
            return False
        if not self.lastname:
            return False
        return True

    def is_email_valid(self):
        if not ("@" in self.email):
            return False
        if not ("." in self.email):
            return False
        return True

    def is_content_valid(self):
        if not self.subject:
            return False
        if not self.message:
            return False
        return True

    def print_form(self):
        print(self.firstname + " " + self.lastname)
        print(self.email)
        print(self.company)
        print(self.subject)
        print(self.message)