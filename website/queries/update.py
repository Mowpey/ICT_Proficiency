from flask import Blueprint,request,redirect,url_for,flash,render_template,send_file
from .. import Session, db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable,UserAssessment
from sqlalchemy import select,update
import io
from datetime import datetime
import magic
from ..queries import insert_history
update_bp = Blueprint('update',__name__)


# If a new PDF was uploaded, update the applicant_form field
def is_pdf(applicant_attachment):

    mime = magic.Magic(mime=True)
    applicant_attachment_isValid = applicant_attachment.read(2048)
    applicant_attachment.seek(0)
    return mime.from_buffer(applicant_attachment_isValid) == 'application/pdf'


@update_bp.route('/<int:applicant_id>',methods = ['POST'])
def updateValues(applicant_id):

    diagnostic_form_data = update(DiagnosticResults).where(DiagnosticResults.applicant_id
        == applicant_id).values(
            first_name = request.form.get('first_name', '').strip() or None,
            middle_name = request.form.get('middle_name', '').strip() or None,
            last_name = request.form.get('last_name', '').strip() or None,
            sex = request.form.get('sex', '').strip() or None,
            province = request.form.get('province', '').strip() or None,
            venue_address = request.form.get('venue_address','').strip() or None,
            exam_venue = request.form.get('exam_venue', '').strip() or None,
            date_of_examination = datetime.strptime(request.form.get('date_exam', ''), '%B %d, %Y').date() if request.form.get('date_exam') else None,
            date_of_notification = datetime.strptime(request.form.get('date_notified', ''), '%B %d, %Y').date() if request.form.get('date_notified') else None,
            proctor = request.form.get('proctor', '').strip() or None,
            status = request.form.get('status', '').strip() or None,
            contact_number = request.form.get('contact_number', '').strip() or None,
            email_address = request.form.get('email_address', '').strip() or None,
            part_one_score = request.form.get('part_one_score', '').strip() or None,
            part_two_score = request.form.get('part_two_score', '').strip() or None,
            part_three_score = request.form.get('part_three_score', '').strip() or None,
            total_score = request.form.get('total_score', '').strip() or None,
        )

    new_applicant_form = request.files.get('edit_applicant_attachment') #checks if a new file is uploaded


    if new_applicant_form and is_pdf(new_applicant_form):
        new_pdf = update(DiagnosticResults).where(DiagnosticResults.applicant_id == applicant_id).values(
            applicant_form=new_applicant_form.read()
        )
        db.session.execute(new_pdf)
        db.session.commit()
    else:
        flash("The file is not a valid PDF File. Only PDF files are accepted!", 'diagnostic_error')
        return redirect(url_for('views.showDiagnosticTable'))

    db.session.execute(diagnostic_form_data)
    insert_history.add_diagnostic_edit_history(request.form['first_name'], request.form['last_name'])
    db.session.commit()
    flash("Diagnostic Record has been updated successfully",'diagnostic_success')
    return redirect(url_for('views.showDiagnosticTable'))



@update_bp.route('/update_handson/<int:applicant_id>',methods = ['POST'])
def updateValues_handson(applicant_id):
    handson_form_data = update(HandsonResults).where(HandsonResults.applicant_id == applicant_id).values(
        exam_venue=request.form.get('exam_venue'),
        venue_address = request.form.get('venue_address','').strip() or None,
        date_of_examination=datetime.strptime(request.form.get('date_exam', ''), '%B %d, %Y').date(),
        date_of_notification=datetime.strptime(request.form.get('date_notified', ''), '%B %d, %Y').date(),
        proctor=request.form.get('proctor'),
        handson_score=request.form.get('handson_score'),
        status=request.form.get('status')
    )
    diagnostic_total_data = update(DiagnosticResults).where(
        DiagnosticResults.applicant_id == applicant_id).values(
            part_one_score = request.form.get('part_one_score', '').strip() or None,
            part_two_score = request.form.get('part_two_score', '').strip() or None,
            part_three_score = request.form.get('part_three_score', '').strip() or None,
            total_score = request.form.get('total_score', '').strip() or None,
        )
    db.session.execute(handson_form_data)
    db.session.execute(diagnostic_total_data)
    insert_history.add_handson_edit_history(applicant_id)
    db.session.commit()
    flash("Handson Record has been updated successfully",'handson_success')
    return redirect(url_for('views.showHandsonTable'))


@update_bp.route('/view_attachment/<int:applicant_id>', methods = ['GET'])
def view_attachment(applicant_id):
    diagnostic_query = select(DiagnosticResults).where(DiagnosticResults.applicant_id == applicant_id)
    diagnostic_result = db.session.execute(diagnostic_query).scalar_one_or_none()

    if diagnostic_result and diagnostic_result.applicant_form:
        return send_file(
            io.BytesIO(diagnostic_result.applicant_form),
            mimetype='application/pdf',
            as_attachment=False,
        )
    user_assessment_query = select(UserAssessment).where(UserAssessment.applicant_id == applicant_id)
    user_assessment_result = db.session.execute(user_assessment_query).scalar_one_or_none()

    if user_assessment_result and user_assessment_result.applicant_form:
        return send_file(
            io.BytesIO(user_assessment_result.applicant_form),
            mimetype='application/pdf',
            as_attachment=False,
        )
    return redirect(url_for('views.showDiagnosticTable'))


@update_bp.route('/update_assessment/<int:applicant_id>',methods = ['POST'])
def updateValues_assessment(applicant_id):
    assessment_form_data = update(UserAssessment).where(UserAssessment.applicant_id == applicant_id).values(
        first_name=request.form.get('first_name', '').strip() or None,
        middle_name=request.form.get('middle_name', '').strip() or None,
        last_name=request.form.get('last_name', '').strip() or None,
        sex=request.form.get('sex', '').strip() or None,
        province=request.form.get('province', '').strip() or None,
        contact_number=request.form.get('contact_number', '').strip() or None,
        email_address=request.form.get('email_address', '').strip() or None,
        exam_venue=request.form.get('exam_venue', '').strip() or None,
        venue_address=request.form.get('venue_address', '').strip() or None,
        date_of_examination=datetime.strptime(request.form.get('date_exam', ''), '%B %d, %Y').date() if request.form.get('date_exam') else None,
        date_of_notification=datetime.strptime(request.form.get('date_notified', ''), '%B %d, %Y').date() if request.form.get('date_notified') else None,
        proctor=request.form.get('proctor', '').strip() or None,
        status=request.form.get('status', '').strip() or None,
        remarks=request.form.get('remarks', '').strip() or None,
        assessment_score=request.form.get('assessment_score', '').strip() or None
    )
    
    new_applicant_form = request.files.get('applicant_attachment')
    if new_applicant_form and is_pdf(new_applicant_form):
        new_pdf = update(UserAssessment).where(UserAssessment.applicant_id == applicant_id).values(
            applicant_form=new_applicant_form.read()
        )
        db.session.execute(new_pdf)
    else:
        flash("The file is not a valid PDF File. Only PDF files are accepted!", 'assessment_error')
        return redirect(url_for('views.showAssessmentTable'))

    db.session.execute(assessment_form_data)
    db.session.commit()
    flash("Assessment Record has been updated successfully",'assessment_success')
    return redirect(url_for('views.showAssessmentTable'))
    
