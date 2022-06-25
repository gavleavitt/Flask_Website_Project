"""
Top level module for Flask flask_application, kicks off app.
Flask flask_application "flask_application" is a member of the "flask_application" package and is read from the __init__ file when importing from the
flask_application package.

"""
import sys
import os
import logging
sys.path.insert(0,'..')
sys.path.append('../..')
sys.path.append('/var/www/myapp/src')
sys.path.append('/home/gavin_admin/docker/flaskapp/Flask_Application/Flask/flask_application')
from flask_application import application

# load_dotenv()
if __name__ == "__main__":
    application.run()


