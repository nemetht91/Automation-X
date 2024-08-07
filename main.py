import time

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from os import environ
from forms import *
from notifier_manager import NotifierManger
from datetime import datetime, date
import sqlalchemy.exc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from settings import *
import logging

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'

##CONNECT TO DB
engine = sqlalchemy.create_engine(DATABASE_STRING, pool_pre_ping=True, pool_size=10, max_overflow=20, pool_recycle=300,
                                  connect_args={
                                      "keepalives": 1,
                                      "keepalives_idle": 30,
                                      "keepalives_interval": 10,
                                      "keepalives_count": 5,
                                  }
                                  )

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
    img_url = db.Column(db.Text, nullable=False)
    tag_robot = db.Column(db.Boolean, nullable=True)
    tag_cobot = db.Column(db.Boolean, nullable=True)
    tag_amr = db.Column(db.Boolean, nullable=True)
    tag_simulation = db.Column(db.Boolean, nullable=True)
    tag_consultancy = db.Column(db.Boolean, nullable=True)
    date = db.Column(db.String(250), nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    benefit1 = db.Column(db.Text, nullable=True)
    benefit2 = db.Column(db.Text, nullable=True)
    benefit3 = db.Column(db.Text, nullable=True)
    benefit4 = db.Column(db.Text, nullable=True)
    benefit5 = db.Column(db.Text, nullable=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


with app.app_context():
    #print('sqlalchemy engine:', db.engine)
    try:
        db.create_all()
        db.session.commit()

        # close the sql pool connections so that new forks create their own connection.
        db.session.remove()
        db.engine.dispose()
    except sqlalchemy.exc.OperationalError as e:
        logging.warning("Database Connection error: ")
        logging.error(e)
        db.session.rollback()


def get_admin_user():
    try:
        admin = User.query.get(1)
        return admin
    except sqlalchemy.exc.OperationalError as e:
        logging.warning("Database Connection error: ")
        logging.error(e)
        logging.warning("Failed to fetch admin user: ")


def create_admin_user():
    with app.app_context():
        admin = get_admin_user()
        if not admin:
            try:
                admin = User(
                    username=ADMIN_USERNAME,
                    password=ADMIN_PASSWORD
                )
                db.session.add(admin)
                db.session.commit()
                db.session.remove()
                db.engine.dispose()
            except sqlalchemy.exc.IntegrityError:
                return None
            except sqlalchemy.exc.OperationalError as e:
                logging.warning("Database Connection error: ")
                logging.error(e)
                logging.warning("Failed to create admin user: ")
                return None


create_admin_user()


@app.route('/')
def get_home():
    return render_template("index.html")


@app.route('/services')
def get_services():
    case_studies = fetch_case_studies()
    sorted_case_studies = sort_case_studies(case_studies)
    return render_template("services.html", case_studies=sorted_case_studies)


def fetch_case_studies():
    db.session.remove()
    db.engine.dispose()
    error_counter = 0
    case_studies = None
    while is_keep_going(case_studies, error_counter):
        try:
            case_studies = CaseStudy.query.order_by(desc(CaseStudy.id)).all()
        except sqlalchemy.exc.OperationalError as e:
            error_counter = error_counter + 1
            logging.warning("Database Connection error: ")
            logging.error(e)
            db.session.rollback()
            logging.warning("Attempting to reconnect")
            time.sleep(1)
            db.session.begin()
    return case_studies


def fetch_case_study(case_study_id):
    db.session.remove()
    db.engine.dispose()
    error_counter = 0
    case_study = None
    while is_keep_going(case_study, error_counter):
        try:
            case_study = CaseStudy.query.get(case_study_id)
        except sqlalchemy.exc.OperationalError as e:
            error_counter = error_counter + 1
            logging.warning("Database Connection error: ")
            logging.error(e)
            db.session.rollback()
            logging.warning("Attempting to reconnect")
            time.sleep(1)
            db.session.begin()
    return case_study


def is_keep_going(data, error_counter):
    if data is not None:
        return False
    if error_counter > 1:
        return False
    return True


def sort_case_studies(case_studies: [CaseStudy]):
    if not case_studies:
        return []
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
    case_studies = fetch_case_studies()
    if case_studies is None:
        case_studies = []
    return render_template("projects.html", case_studies=case_studies)


@app.route("/casestudy/<int:case_study_id>")
def get_case_study(case_study_id):
    case_study = fetch_case_study(case_study_id)
    if not case_study:
        return redirect(url_for("get_projects"))
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
    with app.app_context():
        case_study = fetch_case_study(case_study_id)
        if not case_study:
            return redirect(url_for("get_projects"))
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
    case_study.date = date.today().strftime("%d %B %Y")
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
    case_study = fetch_case_study(case_study_id)
    if not case_study:
        return redirect(url_for("get_projects"))
    return render_template("delete.html", case_study=case_study)


@app.route("/delete/<int:case_study_id>")
@login_required
def delete_case_study(case_study_id):
    with app.app_context():
        case_study = fetch_case_study(case_study_id)
        if not case_study:
            return redirect(url_for("get_projects"))
        db.session.delete(case_study)
        db.session.commit()
    return redirect(url_for("get_projects"))


@app.route('/3f93aa183e12loginc25f80099189', methods=["GET", "POST"])
def get_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if login(username, password):
            return redirect(url_for("get_projects"))
        flash("Incorrect username or password", "error")
    return render_template("login.html")


def login(username, password):
    with app.app_context():
        user = get_user(username)
        if user is None:
            return False
        if check_password_hash(user.password, password):
            login_user(user)
            return True
        return False


def get_user(username):
    try:
        return User.query.filter_by(username=username).first()
    except sqlalchemy.exc.OperationalError as e:
        logging.error("Database connection lost")
        logging.error(e)
        return None


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_projects'))


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except sqlalchemy.exc.OperationalError as e:
        logging.error("Database connection lost")
        logging.error(e)
        return None


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
