from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'You wish you knew'

task_list = ['Learn Flask', 'Learn SQL', 'Learn Django']

class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    submit = SubmitField('Add Task')

@app.route('/', methods=['GET', 'POST'])
def index():
    task_form = TaskForm()
    if task_form.validate_on_submit():
        task_list.append(task_form.task.data)
        return redirect(url_for('index'))
    return render_template('index.html', todos = task_list, template_form = task_form)