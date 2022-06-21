"""
Top level module for Flask application, kicks off app.
Flask application "application" is a member of the "application" package and is read from the __init__ file when importing from the
application package. 

"""
import sys
import os
import logging
sys.path.insert(0,'..')
sys.path.append('../..')
sys.path.append('/var/www/myapp/src')
sys.path.append('/home/gavin_admin/docker/flaskapp/Flask_Application/Flask/application')
print(f"System path is: {sys.path}", file=sys.stdout)
from application import application
#print(os.environ.get('PYTHONPATH', ''))
# try:
#     from application import application
# except:
#     try:
#         from Flask.application import application
#     except:
#         pass
#     try:
#         from Flask import application
#     except:
#         pass
#     try:
#         from Flask_Application.Flask.application import application
#     except:
#         pass
#     try:
#         from Flask_Application.Flask.application import application
#     except:
#         pass
#from Flask_Application.Flask.application import application
#from application import application
#sys.path.append('/path/to/pkg1')
#from dotenv import load_dotenv


# load_dotenv()
if __name__ == "__main__":
    application.run()


