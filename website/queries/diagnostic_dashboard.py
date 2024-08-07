from flask import Blueprint, request, render_template
from .. import db, engine
from ..models import DiagnosticResults
from sqlalchemy import select
from datetime import datetime, date
from sqlalchemy import select, func, case

diagnostic_dashboard = Blueprint('diagnostic_dashboard', __name__)

def get_dashboard_data(start_date=None, end_date=None):
    with db.session() as session:
        if not start_date:
            start_date = date(2024, 1, 1)  
        if not end_date:
            end_date = date.today()

        date_filter = DiagnosticResults.date_of_examination.between(start_date, end_date)

        count_query = select(
            func.count().label('total_applicants'),
            func.sum(case((DiagnosticResults.status == 'Passed', 1), else_=0)).label('passed_count'),
            func.sum(case((DiagnosticResults.status == 'Failed', 1), else_=0)).label('failed_count')
        ).where(date_filter)

        counts = session.execute(count_query).first()

        province_query = select(
            DiagnosticResults.province,
            func.count().label('passed_count')
        ).where(
            date_filter,
            DiagnosticResults.status == 'Passed'
        ).group_by(DiagnosticResults.province)

        passers_per_province = session.execute(province_query).all()

        return {
            'total_applicants': counts.total_applicants,
            'passed_count': counts.passed_count,
            'failed_count': counts.failed_count,
            'passers_per_province': dict(passers_per_province)
        }

@diagnostic_dashboard.route('/dashboard', methods=['GET', 'POST'])
def filterdashboard():
    if request.method == 'POST':
        datestart = request.form.get('filter_date_exam_start')
        dateend = request.form.get('filter_date_exam_end')


        if datestart and dateend:
            start_date = datetime.strptime(datestart, '%B %d, %Y').date()
            end_date = datetime.strptime(dateend, '%B %d, %Y').date()
            results = get_dashboard_data(start_date, end_date)
        else:
            results = get_dashboard_data()
    else:
        results = get_dashboard_data()

    return render_template("dashboard.html", active_page="dashboard", results=results,datestart = datestart,dateend = dateend)