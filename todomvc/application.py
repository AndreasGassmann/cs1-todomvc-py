from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
cors = CORS(app, resources={r"*": {'origins': '*',
                                   'headers': 'content-type',
                                   'methods': 'GET, PUT, POST, DELETE'}})
