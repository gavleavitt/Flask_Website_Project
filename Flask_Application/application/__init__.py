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
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup logger
logger = logging.getLogger(__name__)
# Set time and message format of logs
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# Set Logger to debug level
logger.setLevel(logging.DEBUG)
# Set logging pathway depending on if Flask is running local or on AWS EB on Amazon Linux 2
if "B:\\" in os.getcwd():
    dirname = os.path.dirname(__file__)
    # handler = RotatingFileHandler(os.path.join(dirname, '../logs/application.log'), maxBytes=1024, backupCount=5)
    handler = logging.FileHandler(os.path.join(dirname, '../logs/application.log'))
else:
    # see https://stackoverflow.com/a/60549321
    # handler = RotatingFileHandler('/tmp/application.log', maxBytes=1024, backupCount=5)
    handler = logging.FileHandler('/tmp/application.log')
handler.setFormatter(formatter)

# Create flask application, I believe "application" has to be used to work properly on AWS EB
application = app = Flask(__name__)
# Attach logging handler to application
application.logger.addHandler(handler)

application.logger.debug("Python Flask debugger active!")


# # Set up celery client, allows async tasks to be setup
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# # app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# cel_client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# cel_client.conf.update(app.config)


# Setup SQLAlchemy engine sessionmaker factory
engine = create_engine(os.environ.get("DBCON"))
Session = sessionmaker(bind=engine)


# Import project files (initialize them?), imports from the application flask object have to be after flask
# application is initialized to avoid circular imports
# from application import routes, routes_api, models_tracker, parsePDF_WaterQual, StravaWebHook, TestingandDevelopmentRoutes
from application import routes, routes_api
from application.development import testingAndDevelopmentRoutes
# from application.projects import location_tracker, strava_activities, water_quality
from application.projects.water_quality import functionsWaterQual
from application.projects.strava_activities import DBQueriesStrava
# Setup APS scheduler instance
sched = BackgroundScheduler(daemon=True, timezone=utc)

# Setup scheduled tasks
try:
    # Trigger every day at 9:30 am
    # sched.add_job(parsePDF.pdfjob, trigger='cron', hour='9', minute='30')
    # sched.add_job(parsePDF.pdfjob, trigger='cron', hour='15', minute='37')
    # Add PDF parsing job to trigger daily at 4:30 pm UTC, 9:30 PST
    sched.add_job(functionsWaterQual.pdfjob, trigger='cron', hour='16', minute='30')
    # Trigger every minute
    # sched.add_job(parsePDF.pdfjob, 'cron', minute='*')
    # Start scheduled jobs
    sched.start()
    application.logger.debug("Scheduled task created")
except Exception as e:
    application.logger.error("Failed to create parse pdfjob")
    application.logger.error(e)
# Create local public Strava activities topoJSON file
application.logger.debug("Initializing Strava activities TopoJSON.")
DBQueriesStrava.createStravaPublicActTopoJSON()
application.logger.debug("Strava activities TopoJSON has been initialized.")


# Shutdown cron thread if the web process is stopped
atexit.register(lambda: sched.shutdown(wait=False))