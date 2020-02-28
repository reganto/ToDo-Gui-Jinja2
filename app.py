import os
from functools import wraps

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://reganto:540689m$@localhost:3306/todo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(16)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)


class NewForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    text = TextAreaField("Text")
    completed = BooleanField("Completed")


def job_exist(func):
    @wraps(func)
    def wrapper(job_id):
        try:
            job = Job.query.filter(Job.id == job_id).one()
        except Exception:
            return "Invalid Job"
        else:
            return func(job)
     
    return wrapper        


@app.route("/")
def index():
    return redirect(url_for("new"))


@app.route("/new/", methods=["GET", "POST"])
def new():
    form = NewForm()

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        completed = form.completed.data

        job = Job(title=title, text=text, completed=completed)
        db.session.add(job)
        db.session.commit()
        
        return redirect(url_for("incompleted_jobs_list"))
    
    return render_template("new.html", form=form)


@app.route("/incomp/")
def incompleted_jobs_list():
    ijobs = Job.query.filter(Job.completed == False).all()
    return render_template("todo.html", ijobs=ijobs)


@app.route("/comp/")
def completed_jobs_list():
    cjobs = Job.query.filter(Job.completed == True).all()
    return render_template("todo.html", cjobs=cjobs)
  

@app.route("/edit/<int:job_id>/", methods=["GET", "POST"])
@job_exist
def edit(job_id):
    job = job_id

    form = NewForm(title=job.title, text=job.text, completed=job.completed)
    
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        completed = form.completed.data

        job.title = title
        job.text = text
        job.completed = completed

        db.session.add(job)
        db.session.commit()
        return redirect(url_for("incompleted_jobs_list")) 

    return render_template("new.html", form=form)


@app.route("/delete/<int:job_id>/")
@job_exist
def delete(job_id):
    job = job_id

    db.session.delete(job)
    db.session.commit()
    return redirect(url_for("incompleted_jobs_list"))


@app.route("/done/<int:job_id>/")
@job_exist
def done(job_id):
    job = job_id

    job.completed = True
    db.session.add(job)
    db.session.commit()
    
    return redirect(url_for("incompleted_jobs_list"))


@app.route("/back/<int:job_id>/")
@job_exist
def back(job_id):
    job = job_id

    job.completed = False
    db.session.add(job)
    db.session.commit()

    return redirect(url_for("completed_jobs_list"))
