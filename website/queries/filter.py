from flask import Blueprint,request,redirect,url_for,flash,render_template
from .. import Session,db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable
from sqlalchemy import *

filter_bp = Blueprint('filter', __name__)

@filter_bp.route('/apply_filters',methods=['POST'])
def applyFilterDiagnostic():
    filter_stmt = select(DiagnosticResults)

    sort_id = request.form.get('sort_id') 
    sort_name = request.form.get('sort_name')
    sort_sex = request.form.get('sort_sex')
    sort_province = request.form.get('sort_province')
    sort_date_exam = request.form.get('sort_date_exam')
    sort_venue = request.form.get('sort_venue')
    sort_date_notified = request.form.get('sort_date_notified')
    sort_proctor = request.form.get('sort_proctor')
    sort_status = request.form.get('sort_status')

    if sort_id == 'oldest_id':
        filter_stmt = filter_stmt.order_by(DiagnosticResults.applicant_id)
    elif sort_id == 'newest_id':
        filter_stmt = filter_stmt.order_by(desc(DiagnosticResults.applicant_id))

    execute_results = db.session.execute(filter_stmt).scalars().all()

    return render_template('diagnostic_table.html',d_results=execute_results)
    
