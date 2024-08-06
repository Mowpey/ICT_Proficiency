from flask import render_template, make_response, Blueprint, request,redirect,url_for,flash
from ..models import DiagnosticResults,HandsonResults

export_bp = Blueprint('export', __name__)

@export_bp.route('/export-applicant/<int:applicant_id>')
def export_applicant(applicant_id):
    applicant = DiagnosticResults.query.get_or_404(applicant_id)
    handson_details = handson_details = applicant.handson_results
    assessment = assessment  = applicant.user_assessment
    # Render the CSV template
    csv_data = render_template('applicant_export.csv', applicant=applicant,handson_details=handson_details,assessment = assessment)
    
    # Create a response with CSV mimetype
    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=applicant_{applicant_id}.csv'
    
    return response