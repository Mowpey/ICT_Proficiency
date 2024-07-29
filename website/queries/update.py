from flask import Blueprint,request,redirect,url_for,flash,render_template,send_file
from .. import Session, db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable
from sqlalchemy import select,update
import io
from datetime import datetime
import magic

update_bp = Blueprint('update',__name__)


# If a new PDF was uploaded, update the applicant_form field
def is_pdf(applicant_attachment):

    mime = magic.Magic(mime=True)
    applicant_attachment_isValid = applicant_attachment.read(2048)
    applicant_attachment.seek(0)
    return mime.from_buffer(applicant_attachment_isValid) == 'application/pdf'


@update_bp.route('/update_diagnostic/<int:applicant_id>',methods = ['POST'])
def updateValues(applicant_id):

    diagnostic_form_data = update(DiagnosticResults).where(DiagnosticResults.applicant_id
        == applicant_id).values(
            first_name = request.form.get('first_name').strip() if request.form.get('first_name') else None,
            middle_name = request.form.get('middle_name').strip() if request.form.get('middle_name') else None,
            last_name = request.form.get('last_name').strip() if request.form.get('last_name') else None,
            sex = request.form.get('sex').strip() if request.form.get('sex') else None,
            province = request.form.get('province').strip() if request.form.get('province') else None,
            exam_venue = request.form.get('exam_venue').strip() if request.form.get('exam_venue') else None,
            date_of_examination = datetime.strptime(request.form.get('date_exam' ), '%B %d, %Y').date() if request.form.get('date_exam') else None,
            date_of_notification = datetime.strptime(request.form.get('date_notified'), '%B %d, %Y').date() if request.form.get('date_notified') else None,
            proctor = request.form.get('proctor').strip() if request.form.get('proctor') else None,
            status = request.form.get('status').strip() if request.form.get('status') else None,
            contact_number = request.form.get('contact_number').strip() if request.form.get('contact_number') else None,
            email_address = request.form.get('email_address').strip() if request.form.get('email_address') else None,
            part_one_score = request.form.get('part_one_score').strip() if request.form.get('part_one_score') else None,
            part_two_score = request.form.get('part_two_score').strip() if request.form.get('part_two_score') else None,
            part_three_score = request.form.get('part_three_score').strip() if request.form.get('part_three_score') else None,
            total_score = request.form.get('total_score').strip() if request.form.get('total_score') else None
        )

    new_applicant_form = request.files.get('edit_applicant_attachment') #checks if a new file is uploaded


    if new_applicant_form and is_pdf(new_applicant_form):
        # If a new PDF was uploaded, update the applicant_form field
        new_pdf = update(DiagnosticResults).where(DiagnosticResults.applicant_id == applicant_id).values(
            applicant_form=new_applicant_form.read()
        )
        db.session.execute(new_pdf)
        db.session.commit()
        print("new pdf has been committed")

    flash("Applicant Record has been updated successfully",'diagnostic_success')
    db.session.execute(diagnostic_form_data)
    db.session.commit()
    return redirect(url_for('views.showDiagnosticTable'))



@update_bp.route('/update_handson/<int:applicant_id>',methods = ['POST'])
def updateValues_handson(applicant_id):
    handson_form_data = update(HandsonResults).where(HandsonResults.applicant_id == applicant_id).values(
        province=request.form.get('province'),
        exam_venue=request.form.get('exam_venue'),
        date_of_examination=datetime.strptime(request.form.get('date_exam', ''), '%B %d, %Y').date(),
        date_of_notification=datetime.strptime(request.form.get('date_notified', ''), '%B %d, %Y').date(),
        proctor=request.form.get('proctor'),
        handson_score=request.form.get('handson_score'),
        status=request.form.get('status')
    )
    db.session.execute(handson_form_data)
    db.session.commit()
    return redirect(url_for('views.showHandsonTable'))


@update_bp.route('/view_attachment/<int:applicant_id>', methods = ['GET'])
def view_attachment(applicant_id):
    diagnostic_id= select(DiagnosticResults).where(DiagnosticResults.applicant_id == applicant_id)
    result_stmt = db.session.execute(diagnostic_id).scalar_one_or_none()

    if result_stmt and result_stmt.applicant_form:
        return send_file(
            io.BytesIO(result_stmt.applicant_form),
            mimetype='application/pdf',
            as_attachment=False,
        )

    return redirect(url_for('views.showDiagnosticTable'))
