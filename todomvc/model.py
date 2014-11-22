from flask.ext.sqlalchemy import SQLAlchemy
from application import app


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    todos = db.relationship("Todo", uselist=False, backref="user")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Item %r>' % self.name

    def to_dict(self):
        return {"id": self.id, "name": self.name}

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(80))
    completed = db.Column(db.Boolean, nullable=True)
    time_spans = db.relationship("TodoTime", uselist=True, backref="todo")


    def __init__(self, user, subject, completed=False):
        self.user = user
        self.subject = subject
        self.completed = completed

    def __repr__(self):
        return '<Item %r>' % self.name

    def to_dict(self):
        return {"id": self.id, "subject": self.subject, "completed": self.completed}
        #"times": [time_span.to_dict() for time_span in self.time_spans]}

class TodoTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'))
    start = db.Column(db.TIMESTAMP)
    end = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, todo, start, end):
        self.todo = todo
        self.start = start
        self.end = end

    def __repr__(self):
        return '<Item %r>' % self.id

    def to_dict(self):
        return {"id": self.id, "start": self.start, "end": self.end}
        return {"id": self.id, "start": self.start, "end": self.end}