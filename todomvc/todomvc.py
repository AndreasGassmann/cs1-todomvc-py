from datetime import datetime, timedelta
import logging
from random import random

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from flask import request, jsonify, json

from storages import *
from application import app
from model import *


store = ToDoStorage()


@app.route('/')
def api():
    return 'This is the api for our little project'

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    # Get username from cookies
    username = request.cookies.get('username')
    # If no username cookie is set, send error
    if not username:
        return "Please log in first", 403
    else:
        # Check if user set in cookies is valid
        user = User.query.filter_by(name=username).first()
        # If no user is found, send error
        if not user:
            return "Username not found", 404

    # Handle GET requests
    if request.method == 'GET':
        # Get all ToDos of a user
        todo_list = db.session.query(Todo).options(db.joinedload(Todo.time_spans)).filter(Todo.user_id == user.id)
        # Return a list of all ToDos of a user
        return json.dumps(list(todo.to_dict() for todo in todo_list))
    else:
        # Load POST json object into new_todo
        new_todo = request.json
        # Check if new_todo is set, if not, return error
        if not new_todo:
            return "first", 400
        # Check if "subject" is set, if not, return error
        if "subject" not in new_todo:
            return "second", 400

        # Create a new ToDo-Item
        item = Todo(user, new_todo["subject"], new_todo.get("finished"))
        # Add new Todo-Item to DB-Queue
        db.session.add(item)
        # Execute SQL queries
        db.session.commit()
        # Return new item in JSON format
        return jsonify(item.to_dict())


@app.route('/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def todo(todo_id):
    # Get username from cookies
    username = request.cookies.get('username')
    # If no username cookie is set, send error
    if not username:
        return "Please log in first", 403
    else:
        # Check if user set in cookies is valid
        user = User.query.filter_by(name=username).first()
        # If no user is found, send error
        if not user:
            return "Username not found", 404

    # Get specific ToDo
    item = Todo.query.options(db.joinedload(Todo.time_spans)).get(todo_id)
    # Check if result is not empty and returned Item is linked to logged in user, if not, send error
    if item is None or not (item.user_id == user.id):
        return "Not Found", 404

    # Handle GET requests
    if request.method == 'GET':
        # Send item as JSON
        return jsonify(item.to_dict())
    # Handle PUT request
    elif request.method == 'PUT':
        # Load POST json object into new_todo
        new_todo = request.json
        # Check if new_todo is set, if not, return error
        if not new_todo:
            return "first", 400
        # Check if "subject" is set, if not, return error
        if "subject" not in new_todo:
            return "second", 400

        item.name = new_todo["subject"]
        item.description = new_todo.get("completed")

        db.session.commit()
        return jsonify(item.to_dict())
    else:
        db.session.query(Todo).filter(Todo.id == todo_id).delete()
        db.session.commit()

        return 'Item deleted'

@app.route('/todos/<int:todo_id>/times', methods=['GET', 'POST'])
def todoTimes(todo_id):

    # Get username from cookies
    username = request.cookies.get('username')
    # If no username cookie is set, send error
    if not username:
        return "Please log in first", 403
    else:
        # Check if user set in cookies is valid
        user = User.query.filter_by(name=username).first()
        # If no user is found, send error
        if not user:
            return "Username not found", 404

    # Get specific ToDo
    item = Todo.query.options(db.joinedload(Todo.time_spans)).get(todo_id)
    # Check if result is not empty and returned Item is linked to logged in user, if not, send error
    if item is None or not (item.user_id == user.id):
        return "Not Found", 404

    # Handle GET requests
    if request.method == 'GET':
        # Send item as JSON
        return json.dumps(item.to_dict().get("times"))
    # Handle PUT request
    elif request.method == 'POST':
        # Load POST json object into new_todo
        new_todo_time = request.json
        # Check if new_todo_time is set, if not, return error
        if not new_todo_time:
            return "first", 400
        # Check if "start" is set, if not, return error
        if "start" not in new_todo_time:
            return "No start time specified", 400
        # Check if "end" is set, if not, return error
        if "end" not in new_todo_time:
            return "No end time specified", 400

        todoTime = TodoTime(item, new_todo_time["start"], new_todo_time["end"])
        db.session.add(todoTime)
        db.session.commit()
        return jsonify(todoTime.to_dict())

@app.route('/login/<string:username>', methods=['GET', 'POST'])
def login(username):

    user = User.query.filter_by(name=username).first()
    if not user:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    response = app.make_response(json.dumps(user.to_dict()))
    response.set_cookie('username', value=username)
    return response

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = app.make_response("Logged out")
    response.set_cookie('username', '', expires = 0)
    return response


#The following routes are to facilitate debugging
@app.route('/debug/populate', methods=['GET', 'POST'])
def populate():
    todo_list = ['Arrive at venue', 'Listen to tutor', 'Do the Tutorial', 'Eat Pizza', 'Work on the project', 'Win']
    db.drop_all()
    db.create_all()
    user = User("Superman")
    for todo in todo_list:
        item = Todo(user, todo)
        for i in range(0, int(round(random()*10))):
            todoTime = TodoTime(item, datetime.now() + timedelta(minutes=round(random()*100)), datetime.now() + timedelta(minutes=round(random()*100)))
            db.session.add(todoTime)
        db.session.add(item)
    db.session.commit()
    return jsonify(length=len(todo_list))


if __name__ == '__main__':
    debug = False
    # comment this out in production (you would (probably) want to have a config facility, in real life)
    debug = True
    app.run(debug=debug)