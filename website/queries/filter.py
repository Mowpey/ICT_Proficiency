from flask import Blueprint,request,redirect,url_for,flash,render_template
from .. import Session,db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable
from sqlalchemy import *
from datetime import datetime,timedelta

filter_bp = Blueprint('filter', __name__)

@filter_bp.route('/apply_filters', methods=['POST'])
def applyFilterDiagnostic():
    filter_stmt = select(DiagnosticResults)

    filter_conditions = []
    sorting_conditions = []

    sort_id = request.form.get('sort_id')
    sort_name = request.form.get('sort_name')
    sort_sex = request.form.get('sort_sex')
    sort_province = request.form.get('sort_province')
    sort_date_exam = request.form.get('sort_date_exam')
    sort_venue = request.form.get('sort_venue')
    sort_date_notified = request.form.get('sort_date_notified')
    sort_proctor = request.form.get('sort_proctor')
    sort_status = request.form.get('sort_status')


    if sort_id and sort_name:
        flash('Error: You can only use either Sort ID or Sort Name, not both.', 'diagnostic_error')
        return redirect(url_for('views.showDiagnosticTable'))

    #For Sorting Only
    if sort_id == 'oldest_id':
        sorting_conditions.append(DiagnosticResults.applicant_id.asc())
    

    if sort_name == 'asc_name':
        sorting_conditions.append(DiagnosticResults.last_name.asc())
    elif sort_name == 'desc_name':
        sorting_conditions.append(DiagnosticResults.last_name.desc())

    #For Filtering Only
    if sort_sex:
        filter_conditions.append(DiagnosticResults.sex == sort_sex)

    if sort_province:
        filter_conditions.append(DiagnosticResults.province == sort_province)

    if sort_venue:
       filter_conditions.append(or_(
        DiagnosticResults.exam_venue.ilike(f"%{sort_venue}%"),
        DiagnosticResults.venue_address.ilike(f"%{sort_venue}%"),))

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
        end_date = datetime.strptime(end_date, '%B %d, %Y') .date()
        filter_conditions.append(DiagnosticResults.date_of_notification.between(start_date, end_date))
       

    if filter_conditions:
        filter_stmt = filter_stmt.where(and_(*filter_conditions))

    if sorting_conditions:
        filter_stmt = filter_stmt.order_by(*sorting_conditions)

    execute_results = db.session.execute(filter_stmt).scalars().all()

    return render_template('diagnostic_table.html', d_results=execute_results)


