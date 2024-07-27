from flask import Blueprint,render_template
from website.models import *
from sqlalchemy import select,desc
from sqlalchemy.orm import joinedload


views = Blueprint('views', __name__)

@views.route('/')
def showDashboard():
    return render_template("dashboard.html",active_page="dashboard" )

@views.route('/diagnostic_table')
def showDiagnosticTable():
    display_all = select(DiagnosticResults).order_by(desc(DiagnosticResults.applicant_id))
    diagnostic_table_entries = db.session.execute(display_all).scalars().all()
    return render_template("diagnostic_table.html",d_results= diagnostic_table_entries,active_page="table")

@views.route('/handson_table')
def showHandsonTable():
    display_all = (
        select(HandsonResults,DiagnosticResults.first_name,
            DiagnosticResults.middle_name,DiagnosticResults.last_name,
            DiagnosticResults.sex).join(
            DiagnosticResults,HandsonResults.applicant_id ==
            DiagnosticResults.applicant_id).order_by(desc(HandsonResults.applicant_id))


    )
    handson_table_entries = db.session.execute(display_all).mappings().all()
    return render_template("handson_table.html",h_results=handson_table_entries, active_page="table")

@views.route('/history')
def showHistory():
    return render_template("history.html",active_page="history")

@views.route('/handson_dashboard')
def showHandsonDashboard():
    return render_template("handson_dashboard.html",active_page="handson_dashboard")
