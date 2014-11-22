
from flask.ext.sqlalchemy import SQLAlchemy
from application import app


db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120), nullable=True, unique=True)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Item %r>' % self.name