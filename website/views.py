from flask import Blueprint,render_template,request
from flask_sqlalchemy import SQLAlchemy
from website.models import *
from sqlalchemy import select,desc,or_,func
from sqlalchemy.orm import joinedload
from .queries.diagnostic_dashboard import get_dashboard_data
from .queries.handson_dashboard import get_handson_data
from .models import HistoryTable,Admin
from . import views
from flask_login import login_user,login_required,logout_user,current_user,LoginManager
from datetime import datetime,timedelta
from math import ceil

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/dashboard')
@login_required
def showDashboard():
    results = get_dashboard_data()
    return render_template("dashboard.html",active_page="dashboard",results=results )

@views.route('/diagnostic_table')
@login_required
def showDiagnosticTable():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    display_all = select(DiagnosticResults).order_by(desc(DiagnosticResults.applicant_id))
    total_count = db.session.execute(select(func.count(DiagnosticResults.applicant_id))).scalar() or 0
    total_pages = ceil(total_count / per_page)
    offset = (page - 1) * per_page
    diagnostic_table_entries = db.session.execute(display_all.limit(per_page).offset(offset)).scalars().all()
    return render_template("diagnostic_table.html", d_results=diagnostic_table_entries, active_page="table", page=page, total_pages=total_pages)

@views.route('/handson_table')
@login_required
def showHandsonTable():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    display_all = (
        select(HandsonResults, *DiagnosticResults.__table__.columns)
        .join(DiagnosticResults, HandsonResults.applicant_id == DiagnosticResults.applicant_id)
        .order_by(desc(HandsonResults.applicant_id))
    )
    total_count = db.session.execute(select(func.count(HandsonResults.applicant_id))).scalar() or 0
    total_pages = ceil(total_count / per_page)
    offset = (page - 1) * per_page
    handson_table_entries = db.session.execute(display_all.limit(per_page).offset(offset)).mappings().all()
    return render_template("handson_table.html", h_results=handson_table_entries, active_page="table", page=page, total_pages=total_pages)


@views.route('/')
@views.route('/handson_dashboard')
@login_required
def showHandsonDashboard():
    results = get_handson_data()
    return render_template("handson_dashboard.html",active_page="handson_dashboard",results=results)


@views.route('/history', methods=['GET', 'POST'])
@login_required
def showHistory():
    search_query = request.args.get('search', '')
    date_query = request.args.get('date', '')
    admin_query = request.args.get('admin_name', '')
    action_query = request.args.get('action', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = HistoryTable.query

    if search_query:
        query = query.filter(HistoryTable.applicant_name.ilike(f'%{search_query}%'))
    if admin_query:
        query = query.join(Admin).filter(Admin.admin_name == admin_query)
    if action_query:
        query = query.filter(HistoryTable.action_done.ilike(f'%{action_query}%'))

    if date_query:
        start_date, end_date = date_query.split(' - ')
        start_date = datetime.strptime(start_date, '%b %d, %Y').date()
        end_date = datetime.strptime(end_date, '%b %d, %Y').date()
        end_date = end_date + timedelta(days=1)
        query = query.filter(HistoryTable.date_modified >= start_date, HistoryTable.date_modified < end_date)

    query = query.order_by(desc(HistoryTable.date_modified))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    history_entries = pagination.items

    admin_names = {}
    for entry in history_entries:
        if entry.admin_id not in admin_names:
            admin = Admin.query.get(entry.admin_id)
            admin_names[entry.admin_id] = admin.admin_name if admin else "Unknown"
    admin_list = Admin.query.all()
    total_pages = ceil(query.count() / per_page)
    return render_template("history.html",active_page="history",history_entries=history_entries,admin_names=admin_names,admin_list=admin_list,search_query=search_query,date_query=date_query,admin_query=admin_query,action_query=action_query,pagination=pagination,total_pages=total_pages)
