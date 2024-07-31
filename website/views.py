from flask import Blueprint,render_template
from website.models import *
from sqlalchemy import select,desc
from sqlalchemy.orm import joinedload
from .queries.diagnostic_dashboard import get_dashboard_data
from .queries.handson_dashboard import get_handson_data
from .models import HistoryTable 
from . import views

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/dashboard')
def showDashboard():
    results = get_dashboard_data()
    return render_template("dashboard.html",active_page="dashboard",results=results )

@views.route('/diagnostic_table')
def showDiagnosticTable():
    display_all = select(DiagnosticResults).order_by(desc(DiagnosticResults.applicant_id))
    diagnostic_table_entries = db.session.execute(display_all).scalars().all()
    return render_template("diagnostic_table.html",d_results= diagnostic_table_entries,active_page="table")

@views.route('/handson_table')
def showHandsonTable():
    display_all = (
        select(HandsonResults,*DiagnosticResults.__table__.columns).join(
            DiagnosticResults,HandsonResults.applicant_id ==
            DiagnosticResults.applicant_id).order_by(desc(HandsonResults.applicant_id))
    )
    handson_table_entries = db.session.execute(display_all).mappings().all()
    return render_template("handson_table.html",h_results=handson_table_entries, active_page="table")


@views.route('/history')
def showHistory():
    history_entries = HistoryTable.query.all()
    return render_template("history.html",active_page="history",history_entries=history_entries)

@views.route('/')
@views.route('/handson_dashboard')
def showHandsonDashboard():
    results = get_handson_data()
    return render_template("handson_dashboard.html",active_page="handson_dashboard",results=results)
