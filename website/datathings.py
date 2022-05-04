from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db

def fetch_todo():

    #conn = db.connect()
    #query_results = conn.execute("Select * from tasks;").fetchall()
    #conn.close()
    #todo_list = []
    #for result in query_results:
    #    tasks = {
    #        "id": result[0],
    #        "task": result[1],
    #        "status": result[2]
    #    }
    #    todo_list.append(tasks)
    todo_list = [
        {"id": 1, "task": "Task 1", "status": "In Progress"},
        {"id": 2, "task": "Task 2", "status": "Todo"}, \
        ]
    return todo_list

def update_task_entry(task_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()

def update_status_entry(task_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()

def insert_new_task(text: str) ->  int:
    conn = db.connect()
    query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
        text, "Todo")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id

def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From tasks where id={};'.format(task_id)
    conn.execute(query)
    conn.close()