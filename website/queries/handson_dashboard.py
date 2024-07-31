from flask import Blueprint, request, render_template
from .. import db, engine
from ..models import HandsonResults
from sqlalchemy import select
from datetime import datetime, date
from sqlalchemy import select, func, case

handson_dashboard = Blueprint('handson_dashboard', __name__)

def get_handson_data(start_date=None, end_date=None):
    with db.session() as session:
        if not start_date:
            start_date = date(2024, 1, 1)  
        if not end_date:
            end_date = date.today()

        date_filter = HandsonResults.date_of_examination.between(start_date, end_date)

        count_query = select(
            func.count().label('total_applicants'),
            func.sum(case((HandsonResults.status == 'Passed', 1), else_=0)).label('passed_count'),
            func.sum(case((HandsonResults.status == 'Failed', 1), else_=0)).label('failed_count')
        ).where(date_filter)

        counts = session.execute(count_query).first()

        province_query = select(
            HandsonResults.province,
            func.count().label('passed_count')
        ).where(
            date_filter,
            HandsonResults.status == 'Passed'
        ).group_by(HandsonResults.province)

        passers_per_province = session.execute(province_query).all()

        return {
            'total_applicants': counts.total_applicants,
            'passed_count': counts.passed_count,
            'failed_count': counts.failed_count,
            'passers_per_province': dict(passers_per_province)
        }

@handson_dashboard.route('/handson_dashboard', methods=['GET', 'POST'])
def filterdashboard():
    if request.method == 'POST':
        datestart = request.form.get('filter_date_exam_start')
        dateend = request.form.get('filter_date_exam_end')
    
        if datestart and dateend:
            start_date = datetime.strptime(datestart, '%B %d, %Y').date()
            end_date = datetime.strptime(dateend, '%B %d, %Y').date()
            results = get_handson_data(start_date, end_date)
        else:
            results = get_handson_data()
    else:
        results = get_handson_data()

    return render_template("handson_dashboard.html", active_page="handson_dashboard", results=results,datestart = datestart,dateend = dateend)