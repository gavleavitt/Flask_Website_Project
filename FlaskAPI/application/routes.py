from application import application, app
from flask import render_template

@app.route("/")
def index():
    return "Hello world"

@app.route("/about")
def about():
    return "All about Flask"

@app.route("/gps")
def gps():
    return render_template("private/tracker.html")

@app.route("/main")
def main():
    return render_template("public/index.html")

@app.route("/liveviewer")
def testing():
    return render_template("private/tracker_API.html")
