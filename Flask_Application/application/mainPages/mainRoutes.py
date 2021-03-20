"""


@author: Gavin Leavitt
"""

from flask import render_template, Blueprint

mainSite_BP = Blueprint('mainSite_BP', __name__,
                        template_folder='templates',
                        static_url_path='/main/static',
                        static_folder='static')

# @mainSite_BP.route("/main")
@mainSite_BP.route("/")
@mainSite_BP.route("/index")
def index():
    return render_template("index/index.html")

@mainSite_BP.route("/cv")
@mainSite_BP.route("/resume")
def resume():
    return render_template("resume/resume.html")

@mainSite_BP.route("/bio")
@mainSite_BP.route("/about")
def about():
    return render_template("aboutme/aboutme.html")

@mainSite_BP.route("/email")
@mainSite_BP.route("/contact")
@mainSite_BP.route("/contactme")
def contact():
    return render_template("contactme/contactme.html")

# Apply login
# @app.route("/templatetesting")
# def template():
#     return render_template("public/projects/project-template.html")

