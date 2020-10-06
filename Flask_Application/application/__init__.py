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
# from flask_migrate import Migrate
# from application import script_config as dbconfig
import os
import atexit
import time
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
import logging
from logging.handlers import RotatingFileHandler

# setup logger
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger.setLevel(logging.DEBUG)
if "B:\\" in os.getcwd():
    dirname = os.path.dirname(__file__)
    handler = RotatingFileHandler(os.path.join(dirname, '../logs/application.log'), maxBytes=1024, backupCount=5)
else:
    handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024, backupCount=5)
handler.setFormatter(formatter)

# Create flask application, I believe "application" has to be used to work properly on AWS EB
application = app = Flask(__name__)
# Attach handler to application and handler
application.logger.addHandler(handler)

application.logger.debug("Python Flask debugger active!")

# Get environmental variables for AWS RDS connection 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DBCON")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set timezone used by time, set as environmential variable 
# os.environ['TZ'] = 'America/Los_Angeles'
# try:
#     time.tzset()
# except:
#     print("Can't set timezone, on a Windows machine")

# Set up Flask-SQLAlchemy database connection with the Flask app. 
db = SQLAlchemy(app)
# Setup Flask migrate connection with the application and database 
# migrate = Migrate(app, db)

# Imports from the application flask object have to be after flask application is initialized to avoid circular imports
from application import routes, api_routes, models, parsePDF

sched = BackgroundScheduler(daemon=True, timezone=utc)

try:
    # Trigger every day at 9:30 am
    # sched.add_job(parsePDF.pdfjob, trigger='cron', hour='9', minute='30')
    # sched.add_job(parsePDF.pdfjob, trigger='cron', hour='15', minute='37')
    # Trigger at 4:30 pm UTC, 9:30 PST
    sched.add_job(parsePDF.pdfjob, trigger='cron', hour='16', minute='30')
    # Trigger every minute
    # sched.add_job(parsePDF.pdfjob, 'cron', minute='*')
    sched.start()
    application.logger.debug("Scheduled task created")
except Exception as e:
    application.logger.error("Failed to create parse pdfjob")
    application.logger.error(e)

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: sched.shutdown(wait=False))