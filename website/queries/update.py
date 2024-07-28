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


@update_bp.route('/<int:applicant_id>',methods = ['GET','POST'])
def updateValues(applicant_id):

    diagnostic_form_data = update(DiagnosticResults).where(DiagnosticResults.applicant_id
        == applicant_id).values(
            first_name=request.form['first_name'].strip(),
            middle_name=request.form['middle_name'].strip(),
            last_name=request.form['last_name'].strip(),
            sex=request.form['sex'].strip(),
            province=request.form['province'].strip(),
            exam_venue=request.form['exam_venue'].strip(),
            date_of_examination=datetime.strptime(request.form['date_exam'], '%B %d, %Y').date(),
            date_of_notification=datetime.strptime(request.form['date_notified'], '%B %d, %Y').date(),
            proctor=request.form['proctor'].strip(),
            status=request.form['status'].strip(),
            contact_number=request.form['contact_number'].strip(),
            email_address=request.form['email_address'].strip(),
            part_one_score=request.form['part_one_score'].strip(),
            part_two_score=request.form['part_two_score'].strip(),
            part_three_score=request.form['part_three_score'].strip(),
            total_score=request.form['total_score'],
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


    db.session.execute(diagnostic_form_data)
    db.session.commit()
    return redirect(url_for('views.showDiagnosticTable'))








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
