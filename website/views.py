from flask import Blueprint,render_template

views = Blueprint('views', __name__)

@views.route('/')
def showDashboard():
    return render_template("dashboard.html", text="testing", user="Mark")

@views.route('/showTable')
def showTable():
    return render_template("table.html")

@views.route('/showHistory')
def showHistory():
    return render_template("history.html")

