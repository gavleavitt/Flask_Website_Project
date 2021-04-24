from application import SessionLocal
from flask import render_template, Blueprint, request, redirect, url_for, flash
# from application.util.flaskLogin import authenication
from flask_login import login_required, logout_user, current_user, login_user
from .forms import LoginForm
from .models import User
from application import logger

flasklogin_BP = Blueprint('flasklogin_BP', __name__,
                        template_folder='templates',
                        static_folder='static')

# @flasklogin_BP.route('/login-page')
# def loginpage():
#     return render_template('login.html')

@flasklogin_BP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        logger.debug("login request!")
    if current_user.is_authenticated:
        return redirect(url_for('mainSite_BP.index'))
    # Get login form details
    form = LoginForm()
    # Validate login form when submitted
    if form.validate_on_submit():
        # Get submitted username
        user = User.query.filter_by(username=form.username.data).first()
        # Check if username exists in DB, if so hash it and compared to stored hash
        if user is None or not user.check_password(form.password.data):
            # Login failed, flash error message and reload login page
            flash('Invalid username or password')
            return redirect(url_for('flasklogin_BP.login'))
        # Login succeeded, set active and set remember me status
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('mainSite_BP.index'))
    return render_template('login.html', title='Sign In', form=form)


@flasklogin_BP.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('mainSite_BP.index'))