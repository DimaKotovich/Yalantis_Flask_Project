from flask_migrate import Migrate

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_restful import Api


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_data.db?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'

db = SQLAlchemy(app)

api = Api(app)


