from werkzeug.security import generate_password_hash, check_password_hash
from application import Session
from application.util.flaskLogin.models import User

def verify_password(username, password):
    """
    Verifies if the provided username and password are valid.

    The provided username is used to query the DB, if the username is in the DB then the
    username and stored hashed password (hashed in pbkdf2:sha512) are returned to this function.

    The user provided password is then hashed and checked against the stored hash, if they match then the
    username is returned from this function, allowing access to the resource.

    Parameters
    ----------
    username : String
        Username provided by user.
    password : String
        Password provided by user.

    Returns
    -------
    Bool

    """

    session = Session()
    # Get the stored hashed password for the user:
    hashedpass = session.query(User.hashpass).filter(User.user == username).first().hashpass
    session.close()
    # Check provided hash by the hash stored for the user
    return check_password_hash(hashedpass, password)


