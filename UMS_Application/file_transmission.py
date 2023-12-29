from flask import Blueprint, request, send_file, redirect, url_for
from flask_login import login_required, current_user
from UMS_Application.models import SubjectFile, Subject
from io import BytesIO
import zipfile
from UMS_Application.forms import upload_file_form
from UMS_Application import db
from werkzeug.utils import secure_filename

bp = Blueprint('study_material',__name__,url_prefix='/study_material')



@bp.route('/pdf')
@login_required
def get_pdf():
    id = request.args.get('id')
    if id is not None:
        file = SubjectFile.query.get(id)
        if file is not None:
            pdf_buffer = BytesIO(file.Filedata)
            return send_file(pdf_buffer, download_name=file.Name + '.pdf', as_attachment=True, mimetype='application/pdf')
        else:
            return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))

@bp.route('/upload_pdf',methods=['GET','POST'])
@login_required
def upload_new_pdf():
    if current_user.Type == 'faculty' and request.method == 'POST':
        form = upload_file_form()
        if form.validate_on_submit():
            try:
                sub_code = int(request.args.get('sub_code'))
                if sub_code < 0 or sub_code > 10000000 : raise IndexError
            except:
                return redirect(url_for('auth.login'))

            f = form.file.data
            name = secure_filename(f.filename)
            new_name =  name[ : name.rfind('.')]
            data = request.files['file'].read()
            db.session.add(SubjectFile(SubCode=sub_code,Name=new_name,Filedata=data))
            db.session.commit()
            return redirect(url_for('faculty_dashboard.get_subject',subject_id=sub_code))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))
    else:
        if current_user.Type == 'faculty' : return redirect(url_for('faculty_dashboard.index'))
        else : return redirect(url_for('auth.login'))


@bp.route('/update_pdf',methods=['GET','POST'])
@login_required
def update_existing_pdf():
    if current_user.Type == 'faculty' and request.method == 'POST':
        file_id = request.args.get('id')
        form = upload_file_form()
        if form.validate_on_submit():
            try:
                sub_code = int(request.args.get('sub_code'))
                if sub_code < 0 or sub_code > 10000000 : raise IndexError
            except:
                return redirect(url_for('auth.login'))

            f = form.file.data
            name = secure_filename(f.filename)
            new_name =  name[ : name.rfind('.')]
            data = request.files['file'].read()
            existing_file = SubjectFile.query.filter_by(Id=file_id).first()
            existing_file.Name = new_name
            existing_file.Filedata = data
            db.session.commit()
            return redirect(url_for('faculty_dashboard.get_subject',subject_id=sub_code))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))
    else:
        if current_user.Type == 'faculty' : return redirect(url_for('faculty_dashboard.index'))
        else : return redirect(url_for('auth.login'))




@bp.route('/delete')
@login_required
def delete():
    try:
        id = int(request.args.get('id'))
    except:
        id = None
    
    if id is not None:
        file = SubjectFile.query.get(id)
        if file is not None:
            db.session.delete(file)
            db.session.commit()
            sub_code = request.args.get('sub_code')
            return redirect(url_for('faculty_dashboard.get_subject',subject_id=sub_code))
        else:
            return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))


@bp.route('/zip')
@login_required
def get_zip():
    sub_code = request.args.get('sub_code')
    if sub_code is not None:
        files = SubjectFile.query.filter_by(SubCode=sub_code).all()
        subject = Subject.query.filter_by(SubCode=sub_code).first()
        if files is not None and subject is not None:
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer,'w') as f:
                for file in files:
                    pdf_buffer = BytesIO(file.Filedata)
                    f.writestr(f'{file.Name}.pdf',pdf_buffer.getvalue())
                
            zip_buffer.seek(0)
            return send_file(zip_buffer,download_name=f'{subject.Name}.zip',as_attachment=False  ,mimetype='application/zip')
        else:
            return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))