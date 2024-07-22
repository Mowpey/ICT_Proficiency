from flask import Blueprint,render_template

views = Blueprint('views', __name__)

@views.route('/')
def showDashboard():
    return render_template("dashboard.html")

@views.route('/table')
def showTable():
    return render_template("table.html")

@views.route('/history')
def showHistory():
    return render_template("history.html")
