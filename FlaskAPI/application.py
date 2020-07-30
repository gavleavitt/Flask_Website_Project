"""
Top level module for Flask application, kicks off app.
Flask application "application" is a member of the "application" package and is read from the __init__ file when importing from the
application package. 

"""
from application import application

if __name__ == "__main__":
    application.run()
    
