from flask import render_template, make_response, Blueprint,current_app
import werkzeug.exceptions
from ..models import DiagnosticResults,HandsonResults,UserAssessment

export_bp = Blueprint('export', __name__)

@export_bp.route('/export_applicant/<string:applicant_id>')
def export_applicant(applicant_id):
    if applicant_id == 'diagnostic':
        applicants = DiagnosticResults.query.all()

        # Render the CSV template with all applicants' information
        csv_data = render_template('applicant_diagnostic.csv', applicants=applicants)

        # Create a response with CSV mimetype
        response = make_response(csv_data)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=Diagnostic Results.csv'
        return response
    elif applicant_id == 'handson':
        applicants = DiagnosticResults.query.all()
        handson_details = HandsonResults.query.all()
        # Render the CSV template with all applicants' information
        csv_data = render_template('applicant_handson.csv', applicants=applicants,handson_details=handson_details)

        # Create a response with CSV mimetype
        response = make_response(csv_data)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=Hands-on Results.csv'
        return response
    elif applicant_id == 'assessment':
        applicants = UserAssessment.query.all()
        # Render the CSV template with all applicants' information
        csv_data = render_template('applicant_assessment.csv', applicants=applicants)

        # Create a response with CSV mimetype
        response = make_response(csv_data)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=User Assessment Results.csv'
        return response
    else:
        applicant_id = int(applicant_id)
        applicant = DiagnosticResults.query.get(applicant_id)
        handson_details = applicant.handson_results
        assessment = UserAssessment.query.get(applicant_id)
        
        csv_data = render_template('applicant_export.csv', applicant=applicant,handson_details=handson_details,assessment = assessment)

        response = make_response(csv_data)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=applicant_{applicant_id}.csv'
        return response



    