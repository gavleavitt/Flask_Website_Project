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
from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
# Setup logger
logger = logging.getLogger(__name__)
# Set time and message format of logs
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# Set Logger to debug level
logger.setLevel(logging.DEBUG)

# Create flask application, I believe "application" has to be used to work properly on AWS EB
application = app = Flask(__name__)
# Set secret key, this is required for sessions, which allows the server to store user information between requests,
# this is used to enable Flask-Login to function properly
app.secret_key = os.environ.get("SECRET_KEY")

# Set logging pathway depending on if Flask is running local, in development mode, or on AWS EB on Amazon Linux 2
if os.environ['FLASK_ENV'] == "development":
    dirname = os.path.dirname(__file__)
    # handler = RotatingFileHandler(os.path.join(dirname, '../logs/application.log'), maxBytes=1024, backupCount=5)
    handler = logging.FileHandler(os.path.join(dirname, '../logs/application.log'))
    # Set database connection properties
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DBCON_LOCAL")
else:
    # see https://stackoverflow.com/a/60549321
    # handler = RotatingFileHandler('/tmp/application.log', maxBytes=1024, backupCount=5)
    handler = logging.FileHandler('/tmp/application.log')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DBCON_PROD")

# Disabling modification tracking
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
handler.setFormatter(formatter)
# Attach logging handler to application
application.logger.addHandler(handler)
application.logger.debug("Python Flask debugger active")
# set database to use SQLAlchemy
# db = SQLAlchemy()
# Setup SQLAthanor
db = SQLAlchemy(app, model_class = FlaskBaseModel)
# Init flask sqlalchemy database with flask
# db.init_app(app)
db = initialize_flask_sqlathanor(db)

# Setup login manager for Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'flasklogin_BP.login'


# Setup SQLAlchemy engine sessionmaker factory
engine = create_engine(os.environ.get("DBCON"))
Session = sessionmaker(bind=engine)

# Setup SQLAlchemy engine sessionmaker factory for localhost
engineLocal = create_engine(os.environ.get("DBCON_LOCAL"))
SessionLocal = sessionmaker(bind=engineLocal)

# Import project files (initialize them?), imports from the application flask object have to be after flask
# application is initialized to avoid circular imports
# Import HTTP auth
from application.util.flaskAuth.authentication import auth
from application.util import errorEmail
# Import shared assets
# from .util import assets
from .mainPages.mainRoutes import mainSite_BP
from .projectPages.projectPageRoutes import projectPages_BP
from .WebAppProjects.LocationLiveTracker.routes import liveTracker_BP
from .WebAppProjects.LocationLiveTracker.API_Routes import livetrackerAPI_BP
from .WebAppProjects.StravaActivityViewer.API_Routes import stravaActDashAPI_BP
from .WebAppProjects.StravaActivityViewer.routes import stravaActDash_BP
from .WebAppProjects.StravaActivityViewer.API_Admin_Routes import stravaActDashAPI_Admin_BP
from .WebAppProjects.WaterQualityViewer.routes import sbcWaterQuality_BP
from .WebAppProjects.WaterQualityViewer.API_Routes import sbcWaterQualityAPI_BP
from application.WebAppProjects.WaterQualityViewer import functionsWaterQual
from .util.flaskLogin.routes_login import flasklogin_BP
from .util.flaskLogin.models import User
# Register blueprints with application
apiPrefix = '/api/v1'
app.register_blueprint(mainSite_BP)
app.register_blueprint(projectPages_BP)
app.register_blueprint(liveTracker_BP, url_prefix='/webapps/tracker')
app.register_blueprint(livetrackerAPI_BP, url_prefix='/api/v1/tracker')
app.register_blueprint(stravaActDashAPI_BP, url_prefix='/api/v1/activitydashboard')
app.register_blueprint(stravaActDash_BP, url_prefix='/webapps/stravapp')
app.register_blueprint(sbcWaterQuality_BP, url_prefix='/webapps/sbcwaterquality')
app.register_blueprint(sbcWaterQualityAPI_BP, url_prefix='/api/v1/sbcwaterquality')
app.register_blueprint(stravaActDashAPI_Admin_BP, url_prefix='/admin/api/v1/activitydashboard')
app.register_blueprint(flasklogin_BP, url_prefix='/authentication')

# Activate pluggable views
from application.util.ErrorHandling import exception_handler

from application.WebAppProjects.MaintenanceTracking.views import AssetRecAPI, MaintRecAPI, PartInstallRecAPI, \
    stravaRequest
from application.util.APIRegistration import register_api
maintAPIPrefix = f'{apiPrefix}/maintenancetracking'
# Add API views with registration function
# Asset API
register_api(view=AssetRecAPI, endpoint='asset_api', url=f'{maintAPIPrefix}/asset/', pk='rec_id')
# Maintenance Record API
register_api(view=MaintRecAPI, endpoint='maintRec_api', url=f'{maintAPIPrefix}/maintenance/', pk='rec_id')
# Part install API
register_api(view=PartInstallRecAPI, endpoint='partRec_api', url=f'{maintAPIPrefix}/partinstall/', pk='rec_id')
# Strava distance API
# register_api(view=stravaRequest, endpoint='stravadistance_api', url=f'{maintAPIPrefix}/stravadistance/', pk='rec_id')
app.add_url_rule(f'{maintAPIPrefix}/stravadistance/', view_func=stravaRequest, methods=['GET',])

# asset_view = exception_handler(AssetRecAPI.as_view('asset_api'))
# # Attach url routes and methods to the view function and register them with the application
# app.add_url_rule(f'{maintAPIPrefix}/asset/', defaults={'rec_id': None},
#                  view_func=asset_view, methods=['GET',])
# app.add_url_rule(f'{maintAPIPrefix}/asset/', view_func=asset_view, methods=['POST',])
# # Set route to handle requests for specific record IDs
# app.add_url_rule(f'{maintAPIPrefix}/asset/<int:rec_id>', view_func=asset_view,
#                  methods=['GET', 'PUT', 'DELETE'])

# Set up background scheduled task if running in production mode
if os.environ['FLASK_ENV'] != "development":
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
        application.logger.debug("Scheduled tasks created")
    except Exception as e:
        application.logger.error("Failed to create parse pdfjob")
        application.logger.error(e)

    # Shutdown cron thread if the web process is stopped
    atexit.register(lambda: sched.shutdown(wait=False))
    # # Set up celery client, allows async tasks to be setup
    # app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    # # app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    # cel_client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    # cel_client.conf.update(app.config)