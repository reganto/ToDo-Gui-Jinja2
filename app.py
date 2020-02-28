import os

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
  

@app.route("/edit/<int:job_id>/")
def edit(job_id):
    return "edit"


@app.route("/delete/<int:job_id>/")
def delete(job_id):
    return "delete"


@app.route("/done/<int:job_id>/")
def done(job_id):
    return "done"
 
