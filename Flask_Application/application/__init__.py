"""
This init file is opened by MTB_API, it creates the Flask application and sets configuration settings for the app and database connection.
It also sets up the imports for files required by the application.

Creates application object as an instance of class Flask, given the name of the module which called it,
in this case it will be "application"

The application package is defined by the application directory and this init file.

See:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

@Author: Gavin Leavitt

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from application import script_config as dbconfig
import os
import time

# Create flask application, I believe "application" has to be used to work properly on AWS EB
application = app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = (f"postgresql://{dbconfig.settings['user']}:{dbconfig.settings['password']}@{dbconfig.settings['host']}" +
#           f":{dbconfig.settings['port']}/{dbconfig.settings['dbname']}")
# Get environmental variables for AWS RDS connection 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DBCON")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set timezone used by time, set as environmential variable 
os.environ['TZ'] = 'America/Los_Angeles'
time.tzset()
# Set up Flask-SQLAlchemy database connection with the Flask app. 
db = SQLAlchemy(app)
# Setup Flask migrate connection with the application and database 
migrate = Migrate(app, db)

#Imports from the application flask object have to be after flask application is initialized to avoid circular imports
from application import routes, api_routes, models