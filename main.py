from flask import Flask, render_template, redirect, url_for, request
from os import environ


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


@app.route('/contact')
def get_contact():
    return render_template("contact.html")


@app.route('/privacy')
def get_privacy():
    return render_template("privacy.html")


if __name__ == "__main__":
    app.run(debug=True)
