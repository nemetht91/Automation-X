from flask import Flask, render_template, redirect, url_for, request
from os import environ
from forms import *
from notifier_manager import NotifierManger


app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")


@app.route('/')
def get_home():
    return render_template("index.html")


@app.route('/services')
def get_services():
    return render_template("services.html")


@app.route('/projects')
def get_projects():
    return render_template("projects.html")


@app.route('/about')
def get_about():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def get_contact():
    if request.method == "POST":
        contact_form = ContactForm(request.form)
        is_success = process_form(contact_form)
        if not is_success:
            return render_template("failed.html")
        return render_template("success.html")
    return render_template("contact.html")


@app.route('/privacy')
def get_privacy():
    return render_template("privacy.html")


@app.route('/success')
def get_success():
    return render_template("success.html")


@app.route('/failed')
def get_failed():
    return render_template("failed.html")


def process_form(form: ContactForm):
    if not form.is_valid():
        return False
    notifier = NotifierManger()
    return notifier.send_email(form)


if __name__ == "__main__":
    app.run(debug=True)
