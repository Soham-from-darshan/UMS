from UMS_Application.models import User,Student,Faculty
from UMS_Application import login_manager
from flask_login import login_user, login_required, logout_user,current_user
from flask import Blueprint, redirect,url_for, render_template,flash, current_app
import UMS_Application.forms as forms

bp = Blueprint('auth',__name__)



@login_manager.user_loader
def load_user(user_id):
    user =  User.query.get(int(user_id))
    if user.Type == 'student' : return Student.query.filter_by(UserId = user.UserId).first() 
    elif user.Type == 'faculty' : return Faculty.query.filter_by(UserId = user.UserId).first()



@bp.route('/',methods=['GET','POST'])
def login():
    login_form = forms.login_form()
    if login_form.validate_on_submit():
        if login_form.email.data == current_app.config['ADMIN_EMAIL'] and login_form.password.data == current_app.config['ADMIN_PASSWORD']:
            return redirect(url_for('admin.home'))
        
        user = User.query.filter_by(Email=login_form.email.data,Password=login_form.password.data).first()

        if user is not None:
            login_user(load_user(user.UserId))
            if current_user.Type == 'student' : return redirect(url_for('student_dashboard.index'))
            else : return redirect(url_for('faculty_dashboard.index'))
        else:
            flash('Bad credentials  :(')
    
    return render_template('authentication/login.html',form=login_form)



@bp.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
