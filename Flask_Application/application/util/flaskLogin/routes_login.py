from application import SessionLocal
from flask import render_template, Blueprint, request, redirect, url_for, flash
from application.util.flaskLogin import authenication

flasklogin_BP = Blueprint('flasklogin_BP', __name__,
                        template_folder='templates',
                        static_folder='static')



@flasklogin_BP.route('/login', methods=['POST'])
def login():
    user = request.form.get('user')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    if authenication.verify_password(user, password):
        redirect(url_for('mainSite_BP.index'))
    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('/login'))


@flasklogin_BP.route('/logout')
def logout():
    return "Logout"