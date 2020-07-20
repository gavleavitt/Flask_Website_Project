"""
Top level module for Flask application, kicks off app.
Flask application "app" is a member of the "application" package and is read from the __init__ file when importing from the
application package. 
"""
from application import app

if __name__ == "__main__":
    app.run()
    
