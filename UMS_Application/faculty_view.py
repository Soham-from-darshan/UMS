from flask import Blueprint,render_template, url_for, request, redirect
from flask_login import login_required, current_user
from UMS_Application.models import FacultySubject, Faculty, Subject, SubjectFile
import base64
from UMS_Application.forms import upload_file_form

bp = Blueprint('faculty_dashboard',__name__,url_prefix='/faculty_dashboard')



@bp.route('/')
@login_required
def index():
    fac_subjects = FacultySubject.query.filter_by(FacId=current_user.FacultyId).all()
    subjects = [Subject.query.filter_by(SubCode=sub.SubId).first() for sub in fac_subjects]
    return render_template('Dashboards/faculty/dashboard.html',btoa=base64.b64encode,subjects=subjects,faculty=current_user)



@bp.route('/profile')
@login_required
def profile():
    hidden_fields = ['UserId','FacultyId','Type','Image']
    details = {}
    
    for column in Faculty.__table__.columns:
        if column.name not in hidden_fields:
            column_value = getattr(current_user, column.name)
            details[column.name] = column_value

    return render_template('Dashboards/faculty/profile.html',faculty=current_user,details=details,btoa=base64.b64encode)



@bp.route('/subject')
@login_required
def get_subject():
    try:
        subject_id = int(request.args.get('subject_id'))
    except:
        subject_id = -1

    subject = Subject.query.filter_by(SubCode=str(subject_id)).first()

    if subject is not None:
        subject_files = SubjectFile.query.filter_by(SubCode=subject_id).all()
        subject_files = zip(subject_files,list(range(1,len(subject_files)+1)))
        file_upload_form = upload_file_form()
        return render_template('Dashboards/faculty/subject.html',subject=subject,subject_files=subject_files ,faculty=current_user,btoa=base64.b64encode,form=file_upload_form)
    else:
        return redirect(url_for('faculty_dashboard.index'))

