"""
See https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Creates application object as an instance of class Flask, given the name of the module which called it,
in this case it will "application"

The application package is defined by the application directory and this init file.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from application import script_config as dbconfig

# from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (f"postgresql://{dbconfig.settings['user']}:{dbconfig.settings['password']}@{dbconfig.settings['host']}" +
          f":{dbconfig.settings['port']}/{dbconfig.settings['dbname']}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['BASIC_AUTH_USERNAME'] = dbconfig.creds['postuser']
# app.config['BASIC_AUTH_PASSWORD'] = dbconfig.creds['postpass']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

##Imports from the application flask object have to be after flask application is initialized to avoid circular imports

from application import routes, api_routes, models

#from application import routes

#from application import admin_views
#from application import SQL_Alch
