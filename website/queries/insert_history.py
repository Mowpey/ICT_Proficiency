from flask import Blueprint, request,redirect,url_for,flash,current_app
from .. import Session, db
from ..models import Admin, DiagnosticResults, HandsonResults, HistoryTable,UserAssessment
from datetime import date as d, datetime
import magic
from sqlalchemy import insert
from flask_login import current_user


def add_diagnostic_insert_history(first_name, last_name):
    history_entry = HistoryTable(
        admin_id=current_user.admin_id,
        action_done="Inserted diagnostic data",
        date_modified=datetime.now(),
        applicant_name=f"{first_name} {last_name}"
    )
    db.session.add(history_entry)

def add_handson_insert_history(applicant_id):
    result = DiagnosticResults.query.get(applicant_id)
    applicant_name=f"{result.first_name} {result.last_name}"
    history_entry = HistoryTable(
        admin_id=current_user.admin_id,
        action_done="Inserted handson data",
        date_modified=datetime.now(),
        applicant_name = applicant_name
    )
    db.session.add(history_entry)

def add_diagnostic_edit_history(first_name, last_name):
    history_entry = HistoryTable(
        admin_id=current_user.admin_id,
        action_done="Edited diagnostic data",
        date_modified=datetime.now(),
        applicant_name=f"{first_name} {last_name}"
    )
    db.session.add(history_entry)

def add_handson_edit_history(applicant_id):
    result = DiagnosticResults.query.get(applicant_id)
    applicant_name=f"{result.first_name} {result.last_name}"
    history_entry = HistoryTable(
        admin_id=current_user.admin_id,
        action_done="Edited handson data",
        date_modified=datetime.now(),
        applicant_name = applicant_name
    )
    db.session.add(history_entry)

def add_diagnostic_delete_history(applicant_id):
    result = DiagnosticResults.query.get(applicant_id)
    applicant_name=f"{result.first_name} {result.last_name}"
    history_entry = HistoryTable(
        admin_id=current_user.admin_id,
        action_done="Deleted diagnostic data",
        date_modified=datetime.now(),
        applicant_name = applicant_name
    )
    db.session.add(history_entry)

def add_handson_delete_history(applicant_id):
    result = DiagnosticResults.query.get(applicant_id)
    applicant_name=f"{result.first_name} {result.last_name}"
    history_entry = HistoryTable(
        admin_id=current_user.admin_id,
        action_done="Deleted handson data",
        date_modified=datetime.now(),
        applicant_name = applicant_name
    )
    db.session.add(history_entry)
# user assessment

def add_assessment_edit_history(applicant_id):
    result = UserAssessment.query.get(applicant_id)
    applicant_name=f"{result.first_name} {result.last_name}"
    history_entry = HistoryTable(
        admin_id=current_user.admin_id,
        action_done="Edited User Assessment data",
        date_modified=datetime.now(),
        applicant_name = applicant_name
    )
    db.session.add(history_entry)

def add_assessment_insert_history(first_name, last_name):
    history_entry = HistoryTable(
        admin_id=current_user.admin_id,
        action_done="Inserted diagnostic data",
        date_modified=datetime.now(),
        applicant_name=f"{first_name} {last_name}"
    )
    db.session.add(history_entry)

def add_assessment_delete_history(applicant_id):
    result = UserAssessment.query.get(applicant_id)
    applicant_name=f"{result.first_name} {result.last_name}"
    history_entry = HistoryTable(
        admin_id=current_user.admin_id,
        action_done="Deleted User Assessment data",
        date_modified=datetime.now(),
        applicant_name = applicant_name
    )
    db.session.add(history_entry)