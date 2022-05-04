from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import Tasks
from .models import Event
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            #new_task = Tasks(task=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/todo', methods=['GET','POST'])
def todolist():
    if request.method == 'POST':
        note = request.form.get('task-name')
        if len(note) < 1:
            flash('Task is too short!', category='error')
        else:
            new_task = Tasks(task=note, status='Todo', user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added!', category='success')
    return render_template("todo.html", user=current_user)

@views.route('/create', methods=['POST'])
def create():
    data = request.form.get('description')
    new_task = Tasks(task=data, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@views.route('/update-task', methods=['POST'])
def update_task():
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Tasks.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            if task.status == 'Todo':
                task.status = 'In Progress'
                db.session.commit()
            elif task.status == 'Complete':
                task.status = 'Todo'
                db.session.commit()
            elif task.status == 'In Progress':
                task.status = 'Complete'
                db.session.commit()
            else:
                flash("Woah, how did you get here?", category='error')
    return jsonify({})

@views.route('/delete-task', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Tasks.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
    flash('Task removed', category='success')
    return jsonify({})

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/pomodoroTimer', methods=['GET','POST'])
def pomoTimer():
    return render_template("pomodoro.html", user=current_user)

events = [
    {
        'todo': 'Tutorial for Boris',
        'date': '2022-05-04',
    },
    {
        'todo': 'Finish project',
        'date': '2022-05-07',
    }
]

@views.route('/calendar', methods=['GET','POST'])
def calendar():
    if request.method == 'POST':
        event = request.form.get('event-name')
        date = request.form.get('event-date')

        if len(event) < 1:
            flash('Event name is too short', category='error')
        else:
            new_event = Event(inputDate=date,inputEvent=event,user_id=current_user.id)
            db.session.add(new_event)
            db.session.commit()
            flash('Calendar Event was created!', category='success')
    return render_template("calendar.html", user=current_user)
