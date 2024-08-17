from flask import Blueprint, render_template, request, flash, url_for,redirect
from flask_login import login_required
from sqlalchemy import or_, select, cast, String,extract,func,and_,desc
from .. import db
from website.models import DiagnosticResults,HandsonResults,UserAssessment
from datetime import datetime
from math import ceil
import re

search_bp = Blueprint('search', __name__)

@search_bp.route('/search_diagnostic', methods=['GET', 'POST'])
@login_required
def searchDiagnostic():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    results = []
    if request.method == "POST":
        search_entries = request.form.get("diagnostic_table_input", '').strip()
        if search_entries:
            conditions = []
            for column in DiagnosticResults.__table__.columns:
                if column.name == 'applicant_id':
                    if search_entries.isdigit():
                        conditions.append(column == int(search_entries))

                elif column.name == 'sex':
                    conditions.append(func.lower(column) == func.lower(search_entries))

                elif column.name in ['first_name', 'middle_name', 'last_name', 'province', 'exam_venue', 'venue_address', 'proctor', 'status']:
                    conditions.append(column.ilike(f"%{search_entries}%"))

                elif column.name in ['date_of_examination', 'date_of_notification']:
                    if search_entries.isdigit() and len(search_entries) == 4:
                        conditions.append(extract('year', column) == int(search_entries))
                    elif search_entries.replace(',', ' ').split():
                        date_parts = search_entries.replace(',', ' ').split()
                        year_part = None
                        month_part = None
                        day_part = None
                        for part in date_parts:
                            if part.isdigit():
                                if len(part) == 4:
                                    year_part = int(part)
                                elif 1 <= int(part) <= 31:
                                    day_part = int(part)
                            else:
                                month_part = part.lower()

                        month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                                    'july', 'august', 'september', 'october', 'november', 'december']
                        month_abbr = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                    'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

                        date_conditions = []
                        if month_part:
                            for i, month in enumerate(month_names):
                                if re.search(f'^{month_part}', month, re.IGNORECASE):
                                    month_num = i + 1
                                    date_conditions.append(extract('month', column) == month_num)
                                    break
                            else:
                                for i, month in enumerate(month_abbr):
                                    if re.search(f'^{month_part}', month, re.IGNORECASE):
                                        month_num = i + 1
                                        date_conditions.append(extract('month', column) == month_num)
                        if year_part:
                            date_conditions.append(extract('year', column) == year_part)
                        if day_part:
                            date_conditions.append(extract('day', column) == day_part)
                        if date_conditions:
                            conditions.append(and_(*date_conditions))
                    else:
                        conditions.append(cast(column, String).ilike(f"%{search_entries}%"))
            if conditions:
                stmt = select(DiagnosticResults).where(or_(*conditions))
                total_count = db.session.execute(select(func.count(DiagnosticResults.applicant_id)).where(or_(*conditions))).scalar() or 0
                total_pages = ceil(total_count / per_page)
                offset = (page - 1) * per_page
                results = db.session.execute(stmt.limit(per_page).offset(offset)).scalars().all()

            if not results:
                flash("No results found.", "diagnostic_error")
                return redirect(url_for('views.showDiagnosticTable'))
        else:
            return redirect(url_for('views.showDiagnosticTable'))

    return render_template('diagnostic_table.html', d_results=results, active_page="table", page=page, total_pages=total_pages)


@search_bp.route('/search_handson', methods=['GET', 'POST'])
@login_required
def searchHandson():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    results = []

    if request.method == "POST":
        search_entries = request.form.get("handson_table_input", '').strip()
        if search_entries:
            conditions = []
            for column in HandsonResults.__table__.columns:
                if column.name == 'applicant_id':
                    if search_entries.isdigit():
                        conditions.append(column == int(search_entries))

                elif column.name in ['exam_venue', 'venue_address', 'proctor']:
                    conditions.append(column.ilike(f"%{search_entries}%"))

                elif column.name == 'status':
                    conditions.append(func.lower(column) == func.lower(search_entries))

                elif column.name in ['date_of_examination', 'date_of_notification']:
                        if search_entries.isdigit() and len(search_entries) == 4:
                            conditions.append(extract('year', column) == int(search_entries))
                        elif search_entries.replace(',', ' ').split():
                            date_parts = search_entries.replace(',', ' ').split()
                            year_part = None
                            month_part = None
                            day_part = None
                            for part in date_parts:
                                if part.isdigit():
                                    if len(part) == 4:
                                        year_part = int(part)
                                    elif 1 <= int(part) <= 31:
                                        day_part = int(part)
                                else:
                                    month_part = part.lower()

                            month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                                        'july', 'august', 'september', 'october', 'november', 'december']
                            month_abbr = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                        'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

                            date_conditions = []
                            if month_part:
                                for i, month in enumerate(month_names):
                                    if re.search(f'^{month_part}', month, re.IGNORECASE):
                                        month_num = i + 1
                                        date_conditions.append(extract('month', column) == month_num)
                                        break
                                else:
                                    for i, month in enumerate(month_abbr):
                                        if re.search(f'^{month_part}', month, re.IGNORECASE):
                                            month_num = i + 1
                                            date_conditions.append(extract('month', column) == month_num)
                            if year_part:
                                date_conditions.append(extract('year', column) == year_part)
                            if day_part:
                                date_conditions.append(extract('day', column) == day_part)
                            if date_conditions:
                                conditions.append(and_(*date_conditions))
                        else:
                            conditions.append(cast(column, String).ilike(f"%{search_entries}%"))

            for column in DiagnosticResults.__table__.columns:
                if column.name == 'applicant_id':
                    if search_entries.isdigit():
                        conditions.append(column == int(search_entries))
                elif column.name == 'sex':
                        conditions.append(func.lower(column) == func.lower(search_entries))
                elif column.name in ['first_name', 'middle_name', 'last_name', 'province']:
                        conditions.append(column.ilike(f"%{search_entries}%"))


            if conditions:
                stmt = (select(HandsonResults, *DiagnosticResults.__table__.columns)
                        .join(DiagnosticResults, HandsonResults.applicant_id == DiagnosticResults.applicant_id)
                        .where(or_(*conditions))
                        .order_by(desc(HandsonResults.applicant_id)))

                total_count = db.session.execute(select(func.count(HandsonResults.applicant_id))
                                                 .join(DiagnosticResults, HandsonResults.applicant_id == DiagnosticResults.applicant_id)
                                                 .where(or_(*conditions))).scalar() or 0
                total_pages = ceil(total_count / per_page)
                offset = (page - 1) * per_page
                results = db.session.execute(stmt.limit(per_page).offset(offset)).mappings().all()

            if not results:
                flash("No results found.", "handson_error")
                return redirect(url_for('views.showHandsonTable'))
        else:
            return redirect(url_for('views.showHandsonTable'))

    return render_template('handson_table.html', h_results=results, active_page="table", page=page, total_pages=total_pages)


@search_bp.route('/search_assessment', methods=['GET','POST'])
@login_required
def searchAssessment():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    results = []
    total_pages = 1

    if request.method == "POST":
        search_entries = request.form.get("assessment_table_input", '').strip()
        if search_entries:
            conditions = []
            for column in UserAssessment.__table__.columns:
                if column.name == 'applicant_id':
                    if search_entries.isdigit():
                        conditions.append(column == int(search_entries))
                elif column.name == 'sex':
                    conditions.append(func.lower(column) == func.lower(search_entries))
                elif column.name in ['first_name', 'middle_name', 'last_name', 'province', 'exam_venue', 'venue_address', 'proctor', 'status']:
                    conditions.append(column.ilike(f"%{search_entries}%"))
                elif column.name in ['date_of_examination', 'date_of_notification']:
                    if search_entries.isdigit() and len(search_entries) == 4:
                        conditions.append(extract('year', column) == int(search_entries))
                    elif search_entries.replace(',', ' ').split():
                        date_parts = search_entries.replace(',', ' ').split()
                        year_part = None
                        month_part = None
                        day_part = None
                        for part in date_parts:
                            if part.isdigit():
                                if len(part) == 4:
                                    year_part = int(part)
                                elif 1 <= int(part) <= 31:
                                    day_part = int(part)
                            else:
                                month_part = part.lower()

                        month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                                    'july', 'august', 'september', 'october', 'november', 'december']
                        month_abbr = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                    'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

                        date_conditions = []
                        if month_part:
                            for i, month in enumerate(month_names):
                                if re.search(f'^{month_part}', month, re.IGNORECASE):
                                    month_num = i + 1
                                    date_conditions.append(extract('month', column) == month_num)
                                    break
                            else:
                                for i, month in enumerate(month_abbr):
                                    if re.search(f'^{month_part}', month, re.IGNORECASE):
                                        month_num = i + 1
                                        date_conditions.append(extract('month', column) == month_num)
                        if year_part:
                            date_conditions.append(extract('year', column) == year_part)
                        if day_part:
                            date_conditions.append(extract('day', column) == day_part)
                        if date_conditions:
                            conditions.append(and_(*date_conditions))
                    else:
                        conditions.append(cast(column, String).ilike(f"%{search_entries}%"))
                elif column.name == 'assessment_score':
                    if search_entries.isdigit():
                        conditions.append(column == int(search_entries))

            if conditions:
                stmt = select(UserAssessment).where(or_(*conditions))
                total_count = db.session.execute(select(func.count(UserAssessment.applicant_id)).where(or_(*conditions))).scalar() or 0
                total_pages = ceil(total_count / per_page)
                offset = (page - 1) * per_page
                results = db.session.execute(stmt.limit(per_page).offset(offset)).scalars().all()

            if not results:
                flash("No results found.", "assessment_error")
                return redirect(url_for('views.showAssessmentTable'))
        else:
            return redirect(url_for('views.showAssessmentTable'))

    return render_template('assessment_table.html', a_results=results, active_page="table", page=page, total_pages=total_pages)