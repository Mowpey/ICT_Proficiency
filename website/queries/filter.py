from flask import Blueprint, request, redirect, url_for, flash, render_template
from .. import Session, db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable
from sqlalchemy import *
from datetime import datetime, timedelta
from math import ceil

filter_bp = Blueprint('filter', __name__)

@filter_bp.route('/apply_filters', methods=['POST'])
def applyFilterDiagnostic():
    page = request.args.get('page', 1, type=int)
    per_page = 25

    filter_stmt = select(DiagnosticResults)
    filter_conditions = []

    sort_option = request.form.get('sort_option')
    sort_sex = request.form.get('sort_sex')
    sort_province = request.form.get('sort_province')
    sort_date_exam = request.form.get('sort_date_exam',)
    sort_venue = request.form.get('sort_venue')
    sort_date_notified = request.form.get('sort_date_notified')
    sort_proctor = request.form.get('sort_proctor')
    sort_status = request.form.get('sort_status')

    # Sorting
    if sort_option == 'oldest_id':
        filter_stmt = filter_stmt.order_by(asc(DiagnosticResults.applicant_id))
    elif sort_option == 'asc_name':
        filter_stmt = filter_stmt.order_by(asc(DiagnosticResults.last_name))
    elif sort_option == 'desc_name':
        filter_stmt = filter_stmt.order_by(desc(DiagnosticResults.last_name))

    # Filtering
    if sort_sex:
        filter_conditions.append(DiagnosticResults.sex == sort_sex)
    if sort_province:
        filter_conditions.append(DiagnosticResults.province == sort_province)
    if sort_venue:
        filter_conditions.append(or_(
            DiagnosticResults.exam_venue.ilike(f"%{sort_venue}%"),
            DiagnosticResults.venue_address.ilike(f"%{sort_venue}%"),
        ))
    if sort_status:
        filter_conditions.append(DiagnosticResults.status == sort_status)
    if sort_proctor:
        filter_conditions.append(DiagnosticResults.proctor.ilike(f"%{sort_proctor}%"))
    if sort_date_exam:
        start_date, end_date = sort_date_exam.split(' - ')
        start_date = datetime.strptime(start_date, '%B %d, %Y').date()
        end_date = datetime.strptime(end_date, '%B %d, %Y').date()
        filter_conditions.append(DiagnosticResults.date_of_examination.between(start_date, end_date))
    if sort_date_notified:
        start_date, end_date = sort_date_notified.split(' - ')
        start_date = datetime.strptime(start_date, '%B %d, %Y').date()
        end_date = datetime.strptime(end_date, '%B %d, %Y').date()
        filter_conditions.append(DiagnosticResults.date_of_notification.between(start_date, end_date))

    if filter_conditions:
        filter_stmt = filter_stmt.where(and_(*filter_conditions))
    else:
        filter_stmt = filter_stmt.order_by(desc(DiagnosticResults.applicant_id))

    total_count = db.session.execute(select(func.count(DiagnosticResults.applicant_id))).scalar() or 0
    total_pages = ceil(total_count / per_page)
    offset = (page - 1) * per_page
    execute_results = db.session.execute(filter_stmt.limit(per_page).offset(offset)).scalars().all()

    return render_template('diagnostic_table.html', d_results=execute_results, active_page="table", page=page, total_pages=total_pages)

@filter_bp.route('/apply_filters_handson', methods=['POST'])
def applyFilterHandson():
    page = request.args.get('page', 1, type=int)
    per_page = 25

    filter_stmt = select(HandsonResults, *DiagnosticResults.__table__.columns).join(DiagnosticResults, HandsonResults.applicant_id == DiagnosticResults.applicant_id)
    filtering_conditions = []

    sort_option = request.form.get("sort_option")
    sort_sex = request.form.get('sort_sex')
    sort_province = request.form.get('sort_province')
    sort_date_exam = request.form.get('sort_date_exam')
    sort_venue = request.form.get('sort_venue')
    sort_date_notified = request.form.get('sort_date_notified')
    sort_proctor = request.form.get('sort_proctor')
    sort_status = request.form.get('sort_status')

    # Sorting
    if sort_option == 'oldest_id':
        filter_stmt = filter_stmt.order_by(asc(HandsonResults.applicant_id))
    elif sort_option == 'asc_name':
        filter_stmt = filter_stmt.order_by(asc(DiagnosticResults.last_name))
    elif sort_option == 'desc_name':
        filter_stmt = filter_stmt.order_by(desc(DiagnosticResults.last_name))

    # Filtering
    if sort_sex:
        filtering_conditions.append(DiagnosticResults.sex == sort_sex)
    if sort_province:
        filtering_conditions.append(DiagnosticResults.province == sort_province)
    if sort_date_exam:
        start_date, end_date = sort_date_exam.split(' - ')
        start_date = datetime.strptime(start_date, '%B %d, %Y').date()
        end_date = datetime.strptime(end_date, '%B %d, %Y').date()
        filtering_conditions.append(HandsonResults.date_of_examination.between(start_date, end_date))
    if sort_date_notified:
        start_date, end_date = sort_date_notified.split(' - ')
        start_date = datetime.strptime(start_date, '%B %d, %Y').date()
        end_date = datetime.strptime(end_date, '%B %d, %Y').date()
        filtering_conditions.append(HandsonResults.date_of_notification.between(start_date, end_date))
    if sort_venue:
        filtering_conditions.append(or_(
            HandsonResults.venue_address.ilike(f"%{sort_venue}%"),
            HandsonResults.exam_venue.ilike(f"%{sort_venue}%")
        ))
    if sort_proctor:
        filtering_conditions.append(HandsonResults.proctor.ilike(f"%{sort_proctor}%"))
    if sort_status:
        filtering_conditions.append(HandsonResults.status == sort_status)

    if filtering_conditions:
        filter_stmt = filter_stmt.where(and_(*filtering_conditions))
    else:
        filter_stmt = filter_stmt.order_by(desc(HandsonResults.applicant_id))

    total_count = db.session.execute(select(func.count(HandsonResults.applicant_id))).scalar() or 0
    total_pages = ceil(total_count / per_page)
    offset = (page - 1) * per_page
    execute_results = db.session.execute(filter_stmt.limit(per_page).offset(offset)).all()

    return render_template('handson_table.html', h_results=execute_results, active_page="table", page=page, total_pages=total_pages)
