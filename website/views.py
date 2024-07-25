from flask import Blueprint,render_template

views = Blueprint('views', __name__)

@views.route('/')
def showDashboard():
    return render_template("dashboard.html",active_page="dashboard" )

@views.route('/diagnostic_table')
def showDiagnosticTable():
    return render_template("diagnostic_table.html",active_page="table")

@views.route('/handson_table')
def showHandsonTable():
    return render_template("handson_table.html",active_page="table")

@views.route('/history')
def showHistory():
    return render_template("history.html",active_page="history")

@views.route('/handson_dashboard')
def showHandsonDashboard():
    return render_template("handson_dashboard.html",active_page="handson_dashboard")