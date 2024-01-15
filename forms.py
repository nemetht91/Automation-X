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


class CaseStudyForm:
    def __init__(self, form):
        self.title = form.get("title")
        self.image_url = form.get("image")
        self.tag_robot = form.get("robot")
        self.tag_cobot = form.get("cobot")
        self.tag_amr = form.get("amr")
        self.tag_sim = form.get("simulation")
        self.tag_consultancy = form.get("consultancy")
        self.objectives = form.get("objectives")
        self.solution = form.get("solution")
        self.benefit1 = form.get("benefit1")
        self.benefit2 = form.get("benefit2")
        self.benefit3 = form.get("benefit3")
        self.benefit4 = form.get("benefit4")
        self.benefit5 = form.get("benefit5")

    def print_study(self):
        print(f"Title:\n {self.title}")
        print(f"Image:\n {self.image_url}")
        print(f"Tags - robot: {self.tag_robot}; cobot: {self.tag_cobot}; amr: {self.tag_amr};"
              f"Simulation: {self.tag_sim}; Consultancy: {self.tag_consultancy}")
        print(f"Objectives:\n {self.objectives}")
        print(f"Solution:\n{self.solution}")
        print("Benefits:")
        print(self.benefit1)
        print(self.benefit2)
        print(self.benefit3)
        print(self.benefit4)
        print(self.benefit5)

