from flask import Blueprint,g,render_template, url_for, redirect, request
from flask_login import login_required, current_user
from UMS_Application.models import Student, Subject, SubjectFile, FacultySubject,Faculty
import base64

bp = Blueprint('student_dashboard',__name__,url_prefix='/student_dashboard')



@bp.route('/')
@login_required
def index():
    try:
        sam = int(request.args.get('sam'))
    except:
        sam = 0
    
    if sam not in range(1,current_user.Sam+1):
        sam = current_user.Sam

    subjects = Subject.query.filter_by(Sam = sam).all()

    return render_template('Dashboards/student/dashboard.html',student=current_user,subjects=subjects,selected_sam=sam,btoa=base64.b64encode)



@bp.route('/profile')
@login_required
def profile():
    hidden_fields = ['UserId','StudentId','Income','FeesStatus','HSC_pr','SSC_pr','Batch','RollNo','Type','Image']
    details = {}
    
    for column in Student.__table__.columns:
        if column.name not in hidden_fields:
            column_value = getattr(current_user, column.name)
            details[column.name] = column_value

    return render_template('Dashboards/student/profile.html',student=current_user,details=details,btoa=base64.b64encode)



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

        faculty = FacultySubject.query.filter_by(SubId=subject_id).first()
        faculty = Faculty.query.filter_by(FacultyId=faculty.FacId).first()

        return render_template('Dashboards/student/subject.html',subject=subject,subject_files=subject_files ,student=current_user,faculty=faculty,btoa=base64.b64encode)
    else:
        return redirect(url_for('student_dashboard.index'))