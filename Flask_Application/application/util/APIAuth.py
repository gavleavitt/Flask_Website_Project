from application.util.flaskLogin.models import User
from functools import wraps
from application import login_manager, logger
from flask_login import current_user

# Pluggable views
# https://flask.palletsprojects.com/en/2.0.x/views/
# see https://stackoverflow.com/a/19376449
# for using flask login with pluggable view
def user_required(f):
    """

    @param f:
    @return:
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        # logger.debug(current_user)
        if not current_user.is_authenticated:
            logger.debug(f"Not logged in!")
            return login_manager.unauthorized()
            # or, if you're not using Flask-Login
            # return redirect(url_for('login_page'))
        return f(*args, **kwargs)

    return decorator
