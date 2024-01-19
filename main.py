from flask import Flask, render_template, redirect, url_for, request, flash, abort
from os import environ
from forms import *
from notifier_manager import NotifierManger
from datetime import datetime, date
import sqlalchemy.exc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import desc
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from settings import *
import urllib

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")

##CONNECT TO DB
engine = sqlalchemy.create_engine(DATABASE_STRING, pool_pre_ping=True, pool_size=10, max_overflow=20)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_STRING

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine.dispose()

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)

##CONFIGURE TABLES


class CaseStudy(db.Model):
    __tablename__ = "case_studies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    tag_robot = db.Column(db.Boolean, nullable=True)
    tag_cobot = db.Column(db.Boolean, nullable=True)
    tag_amr = db.Column(db.Boolean, nullable=True)
    tag_simulation = db.Column(db.Boolean, nullable=True)
    tag_consultancy = db.Column(db.Boolean, nullable=True)
    date = db.Column(db.String(250), nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    benefit1 = db.Column(db.String(250), nullable=True)
    benefit2 = db.Column(db.String(250), nullable=True)
    benefit3 = db.Column(db.String(250), nullable=True)
    benefit4 = db.Column(db.String(250), nullable=True)
    benefit5 = db.Column(db.String(250), nullable=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


with app.app_context():
    #print('sqlalchemy engine:', db.engine)
    db.create_all()
    db.session.commit()

    # close the sql pool connections so that new forks create their own connection.
    db.session.remove()
    db.engine.dispose()


def create_admin_user():
    db.engine.dispose()
    with app.app_context():
        admin = User.query.get(1)
        if not admin:
            try:
                admin = User(
                    username=ADMIN_USERNAME,
                    password=ADMIN_PASSWORD
                )
                db.session.add(admin)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                return None


create_admin_user()


@app.route('/')
def get_home():
    return render_template("index.html")


@app.route('/services')
def get_services():
    db.engine.dispose()
    case_studies = CaseStudy.query.order_by(desc(CaseStudy.id)).all()
    sorted_case_studies = sort_case_studies(case_studies)
    return render_template("services.html", case_studies=sorted_case_studies)


def sort_case_studies(case_studies: [CaseStudy]):
    sorted = {}

    robot_studies = [case_study for case_study in case_studies if case_study.tag_robot]
    robot_studies = robot_studies[0:3]
    sorted["robot_studies"] = robot_studies

    cobot_studies = [case_study for case_study in case_studies if case_study.tag_cobot]
    cobot_studies = cobot_studies[0:3]
    sorted["cobot_studies"] = cobot_studies

    amr_studies = [case_study for case_study in case_studies if case_study.tag_amr]
    amr_studies = amr_studies[0:3]
    sorted["amr_studies"] = amr_studies

    sim_studies = [case_study for case_study in case_studies if case_study.tag_simulation]
    sim_studies = sim_studies[0:3]
    sorted["sim_studies"] = sim_studies

    cons_studies = [case_study for case_study in case_studies if case_study.tag_consultancy]
    cons_studies = cons_studies[0:3]
    sorted["cons_studies"] = cons_studies

    return sorted


@app.route('/projects')
def get_projects():
    db.engine.dispose()
    case_studies = CaseStudy.query.order_by(desc(CaseStudy.id)).all()
    return render_template("projects.html", case_studies=case_studies)


@app.route("/casestudy/<int:case_study_id>")
def get_case_study(case_study_id):
    db.engine.dispose()
    case_study = CaseStudy.query.get(case_study_id)
    return render_template("study.html", case_study=case_study)


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


@app.route("/edit/<int:case_study_id>", methods=["GET", "POST"])
@login_required
def edit_case_study(case_study_id):
    db.engine.dispose()
    with app.app_context():
        case_study = CaseStudy.query.get(case_study_id)
        if request.method == "POST":
            update_case_study(case_study, request.form)
            db.session.commit()
            return redirect(url_for("get_case_study", case_study_id=case_study.id))
        return render_template("study_edit.html", case_study=case_study)


def update_case_study(case_study, form):
    case_study.title = form.get("title")
    case_study.img_url = form.get("image")
    case_study.tag_robot = True if form.get("robot") else False
    case_study.tag_cobot = True if form.get("cobot") else False
    case_study.tag_amr = True if form.get("amr") else False
    case_study.tag_simulation = True if form.get("simulation") else False
    case_study.tag_consultancy = True if form.get("consultancy") else False
    case_study.date = date.today().strftime("%B %d, %Y")
    case_study.objectives = form.get("objectives")
    case_study.solution = form.get("solution")
    case_study.benefit1 = form.get("benefit1")
    case_study.benefit2 = form.get("benefit2")
    case_study.benefit3 = form.get("benefit3")
    case_study.benefit4 = form.get("benefit4")
    case_study.benefit5 = form.get("benefit5")


@app.route('/create', methods=["GET", "POST"])
@login_required
def create_case_study():
    if request.method == "POST":
        db.engine.dispose()
        with app.app_context():
            case_study = create_new_case_study(request.form)
            db.session.add(case_study)
            db.session.commit()
        return redirect(url_for("get_projects"))
    return render_template("study_create.html")


def create_new_case_study(form):
    return CaseStudy(
        title=form.get("title"),
        img_url=form.get("image"),
        tag_robot=True if form.get("robot") else False,
        tag_cobot=True if form.get("cobot") else False,
        tag_amr=True if form.get("amr") else False,
        tag_simulation=True if form.get("simulation") else False,
        tag_consultancy=True if form.get("consultancy") else False,
        date=date.today().strftime("%B %d, %Y"),
        objectives=form.get("objectives"),
        solution=form.get("solution"),
        benefit1=form.get("benefit1"),
        benefit2=form.get("benefit2"),
        benefit3=form.get("benefit3"),
        benefit4=form.get("benefit4"),
        benefit5=form.get("benefit5")
    )


@app.route("/delete_confirm/<int:case_study_id>")
@login_required
def get_delete(case_study_id):
    db.engine.dispose()
    case_study = CaseStudy.query.get(case_study_id)
    return render_template("delete.html", case_study=case_study)


@app.route("/delete/<int:case_study_id>")
@login_required
def delete_case_study(case_study_id):
    db.engine.dispose()
    with app.app_context():
        case_study = CaseStudy.query.get(case_study_id)
        db.session.delete(case_study)
        db.session.commit()
    return redirect(url_for("get_projects"))


@app.route('/3f93aa183e12loginc25f80099189', methods=["GET", "POST"])
def get_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if login(username, password):
            flash("Incorrect username or password", "error")
            return redirect(url_for("get_projects"))
    return render_template("login.html")


def login(username, password):
    db.engine.dispose()
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user is None:
            return False
        if check_password_hash(user.password, password):
            login_user(user)
            return True
        return False


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_projects'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


def process_form(form: ContactForm):
    if not form.is_valid():
        return False
    notifier = NotifierManger()
    is_success = notifier.send_enquiry(form)
    if is_success:
        notifier.send_auto_reply(form)
    return is_success


if __name__ == "__main__":
    app.run(debug=False)
