from datetime import timezone
from sqlalchemy.orm import backref
from . import db
from flask_login import UserMixin


class Admin(db.Model,UserMixin):
    admin_id = db.Column(db.Integer,primary_key = True)
    admin_name = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))
    def get_id(self):
        return str(self.admin_id)

class DiagnosticResults(db.Model):
    applicant_id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(128))
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    sex = db.Column(db.String(64))
    province = db.Column(db.String(64))
    exam_venue = db.Column(db.String(64))
    venue_address = db.Column(db.String(128))
    date_of_examination = db.Column(db.Date)
    date_of_notification = db.Column(db.Date)
    proctor = db.Column(db.String(64))
    status = db.Column(db.String(32))
    applicant_form = db.Column(db.LargeBinary)
    contact_number = db.Column(db.String(32))
    email_address = db.Column(db.String(64))
    part_one_score = db.Column(db.Integer)
    part_two_score = db.Column(db.Integer)
    part_three_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    handson_results = db.relationship('HandsonResults',uselist=False,back_populates='diagnostic_results')
   

class UserAssessment(db.Model):
    applicant_id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(128))
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    sex = db.Column(db.String(64))
    province = db.Column(db.String(64))
    exam_venue = db.Column(db.String(64))
    venue_address = db.Column(db.String(128))
    date_of_examination = db.Column(db.Date)
    date_of_notification = db.Column(db.Date)
    proctor = db.Column(db.String(64))
    status = db.Column(db.String(32))
    applicant_form = db.Column(db.LargeBinary)
    contact_number = db.Column(db.String(32))
    email_address = db.Column(db.String(64))
    assessment_score = db.Column(db.Integer)
    remarks = db.Column(db.String(128))
    


class HandsonResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('diagnostic_results.applicant_id'))
    exam_venue = db.Column(db.String(64))
    venue_address = db.Column(db.String(128))
    date_of_examination = db.Column(db.Date)
    date_of_notification = db.Column(db.Date)
    proctor = db.Column(db.String(64))
    handson_score = db.Column(db.Integer)
    status = db.Column(db.String(32))
    diagnostic_results = db.relationship('DiagnosticResults',back_populates="handson_results",uselist=False)

class HistoryTable(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.admin_id'))
    action_done = db.Column(db.String(64))
    date_modified = db.Column(db.DateTime(timezone=True))
    applicant_name = db.Column(db.String(64))
