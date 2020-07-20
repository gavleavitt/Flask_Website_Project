"""
This init file is opened by MTB_API, it creates the flask application and sets configuration settings for the app and database connection.
It also sets up the imports for files required by the application.

Creates application object as an instance of class Flask, given the name of the module which called it,
in this case it will be "application"

The application package is defined by the application directory and this init file.

See:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from application import script_config as dbconfig
import os

application = app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = (f"postgresql://{dbconfig.settings['user']}:{dbconfig.settings['password']}@{dbconfig.settings['host']}" +
#           f":{dbconfig.settings['port']}/{dbconfig.settings['dbname']}")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DBCON")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Imports from the application flask object have to be after flask application is initialized to avoid circular imports
from application import routes, api_routes, models