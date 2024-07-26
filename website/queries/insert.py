from flask import Blueprint, render_template, request,redirect,url_for,flash
from werkzeug.utils import secure_filename
from .. import Session, db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable
from datetime import datetime
import magic 

insert = Blueprint('insert',__name__)

def is_pdf(applicant_attachment):

    applicant_attachment_isValid = applicant_attachment.read(2048)
    applicant_attachment.seek(0)

    mime = magic.Magic(mime=True)
    validFile = mime.from_buffer(applicant_attachment_isValid)

    return validFile == 'application/pdf'

@insert.route('/insert',methods = ['POST'])
def insertTableData():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        sex = request.form['sex']
        province = request.form['province']
        exam_venue = request.form['exam_venue']
        date_of_examination = datetime.strptime(request.form['date_exam'], '%Y-%m-%d')
        date_of_notification = datetime.strptime(request.form['date_notified'], '%Y-%m-%d')
        proctor = request.form['proctor']
        status = request.form['status']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        part_one_score = request.form['part_one_score']
        part_two_score = request.form['part_two_score']
        part_three_score = request.form['part_three_score']
        total_score = request.form['total_score']
        applicant_attachment = request.files['applicant_attachment']
        
        if is_pdf(applicant_attachment):
           file_data = applicant_attachment.read()


        toBeInserted_results = DiagnosticResults(**{k: v for k, v in vars().items() if k in DiagnosticResults.__table__.columns}) #Shorter code instead of manually assigning each result to the database column names
        db.session.add(toBeInserted_results)
        db.session.commit()
    else:
            flash('File type not allowed. Please upload a PDF.')
            return redirect(request.url)


    return redirect(url_for('views.showDiagnosticTable'))