from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from typing import TYPE_CHECKING

app = Flask(__name__)
app.config['SECRET_KEY'] = 'You wish you knew'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
    BaseModel = db.make_declarative_base(Model)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), index=True)

class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    submit = SubmitField('Add Task')

@app.route('/', methods=['GET', 'POST'])
def index():
    task_form = TaskForm()
    if task_form.validate_on_submit():
        new_task = Task(task=task_form.task.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', todos = Task.query.all(), template_form = task_form)

@app.route('/remove/<int:task_id>')
def remove_task(task_id):
    task_to_remove = Task.query.get(task_id)
    db.session.delete(task_to_remove)
    db.session.commit()
    return redirect(url_for('index'))