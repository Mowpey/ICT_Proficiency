from flask import Blueprint,request,redirect,url_for,flash,render_template,send_file
from .. import Session, db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable
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
        # If a new PDF was uploaded, update the applicant_form field
        new_pdf = update(DiagnosticResults).where(DiagnosticResults.applicant_id == applicant_id).values(
            applicant_form=new_applicant_form.read()
        )
        db.session.execute(new_pdf)
        db.session.commit()

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
    db.session.execute(handson_form_data)
    insert_history.add_handson_edit_history(applicant_id)
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
