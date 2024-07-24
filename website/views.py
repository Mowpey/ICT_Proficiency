from flask import Blueprint,render_template

views = Blueprint('views', __name__)

@views.route('/')
def showDashboard():
    return render_template("dashboard.html")
    

@views.route('/diagnostic_table')
def showDiagnosticTable():
    return render_template("diagnostic_table.html")

@views.route('/handson_table')
def showHandsonTable():
    return render_template("handson_table.html")

@views.route('/history')
def showHistory():
    return render_template("history.html")

