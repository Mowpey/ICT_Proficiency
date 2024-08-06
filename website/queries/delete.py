from flask import Blueprint, request,redirect,url_for,flash
from .. import Session, db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable, UserAssessment
from datetime import datetime
import magic
from sqlalchemy import insert,delete,select
from ..queries import insert_history

delete_bp = Blueprint('delete',__name__)

@delete_bp.route('/delete/<int:applicant_id>', methods=['POST'])
def deleteDiagnosticRecord(applicant_id):
        insert_history.add_diagnostic_delete_history(applicant_id)
        db.session.commit()
        diagnostic_form_data = delete(DiagnosticResults).where(DiagnosticResults.applicant_id == applicant_id)
        handson_record = delete(HandsonResults).where(HandsonResults.applicant_id == applicant_id)

        db.session.execute(handson_record)
        db.session.execute(diagnostic_form_data)
        db.session.commit()
        flash('Diagnostic record deleted successfully', 'diagnostic_success')

        return redirect(url_for('views.showDiagnosticTable'))

@delete_bp.route('/delete_handson/<int:applicant_id>', methods=['POST'])
def deleteHandsonRecord(applicant_id):

        handson_record = delete(HandsonResults).where(HandsonResults.applicant_id == applicant_id)

        db.session.execute(handson_record)
        insert_history.add_handson_delete_history(applicant_id)
        db.session.commit()
        flash('Handson record deleted successfully', 'handson_success')

        return redirect(url_for('views.showHandsonTable'))

@delete_bp.route('/delete_assessment/<int:applicant_id>', methods=['POST'])
def deleteAssessmentRecord(applicant_id):

        assessment_record = delete(UserAssessment).where(UserAssessment.applicant_id == applicant_id)

        db.session.execute(assessment_record)
        insert_history.add_assessment_delete_history(applicant_id)
        db.session.commit()
        flash('Assessment record deleted successfully', 'assessment_success')
        return redirect(url_for('views.showAssessmentTable'))
