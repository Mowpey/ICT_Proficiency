from flask import Blueprint, request,redirect,url_for,flash
from .. import Session, db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable
from datetime import datetime
import magic
from sqlalchemy import insert,delete,select

delete_bp = Blueprint('delete',__name__)

@delete_bp.route('/delete/<int:applicant_id>', methods=['POST'])
def deleteDiagnosticRecord(applicant_id):
          
        diagnostic_form_data = delete(DiagnosticResults).where(DiagnosticResults.applicant_id == applicant_id)
        handson_record = delete(HandsonResults).where(HandsonResults.applicant_id == applicant_id)

        db.session.execute(handson_record)
        db.session.execute(diagnostic_form_data)
        db.session.commit()
        flash('Record deleted successfully', 'diagnostic_success')

        return redirect(url_for('views.showDiagnosticTable'))