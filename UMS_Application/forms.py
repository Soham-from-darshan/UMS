from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, FloatField 
from wtforms.validators import InputRequired, Length, DataRequired, ValidationError, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from UMS_Application.models import Student, Faculty, User
from UMS_Application import db

class login_form(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Length(min=2,max=30)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=16)])
    submit = SubmitField('Submit')

class upload_file_form(FlaskForm):
    file = FileField('File',validators=[FileRequired(),FileAllowed(['pdf'],'Only Pdf files are allowed'),FileSize(min_size=10,max_size=2000000)])
    submit = SubmitField('Upload')

class CreateStudentForm(FlaskForm):
    
    user_id = IntegerField('User Id', validators=[DataRequired()])
    enrollment_no = IntegerField('EnrollmentNo', validators=[DataRequired()])
    sam = IntegerField('Semester', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    birthdate = StringField('Birthdate', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    income = FloatField('Income', validators=[DataRequired()])
    mobile_no = IntegerField('Mobile No', validators=[DataRequired()])
    gmail = StringField('Gmail', validators=[DataRequired(), Email()])
    fees_status = StringField('Fees Status', validators=[DataRequired()])
    hsc_pr = FloatField('HSC Percentage', validators=[DataRequired()])
    ssc_pr = FloatField('SSC Percentage', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()])
    class_ = StringField('Class')
    batch = StringField('Batch')
    roll_no = IntegerField('RollNo')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')


    def validate_enrollment_no(form, field):
        user = Student.query.filter(Student.UserId != form.user_id.data, Student.EnrollmentNo == field.data).first()        
        if user :
            raise ValidationError('That Enrollment No is taken. Please choose a different one.')
    
    def validate_roll_no(form, field):
        user = Student.query.filter(Student.UserId != form.user_id.data, Student.RollNo == field.data).first()
        if user:
            raise ValidationError('That RollNo No is taken. Please choose a different one.')
        
    def validate_gmail(form, field):
        user = Student.query.filter(Student.UserId != form.user_id.data, Student.Gmail == field.data).first()
        if user:
            raise ValidationError('That Gmail is taken. Please choose a different one.')
  
    def validate_sam(self, field):
        if not 1 <= field.data <= 8:
            raise ValidationError('Sam must be between 1 and 8.')


#     UserId = Column(Integer, ForeignKey('User.UserId'), primary_key=True, nullable=False)

class CreateFacultyForm(FlaskForm):

    
    user_id = IntegerField('User Id', validators=[DataRequired()])
    faculty_id = IntegerField('Faculty id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    mobile_no = IntegerField('Mobile No', validators=[DataRequired()])
    gmail = StringField('Gmail', validators=[DataRequired(), Email()])
    experience = IntegerField('Experience', validators=[DataRequired()])
    cabin = StringField('Cabin')
    department = StringField('Department', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
    
    # type = StringField('Type', validators=[DataRequired()])

    def validate_gmail(form, field):
        
        faculty = Faculty.query.filter(Faculty.UserId != form.user_id.data, Faculty.Gmail == field.data).first()
        if faculty:
            raise ValidationError('That Gmail is taken. Please choose a different one.')
        else:
            user = User.query.filter(User.UserId == form.user_id.data).first()
            user.Email = field.data
            db.session.commit()
            

class CreateUserForm(FlaskForm):
    type = StringField('Type', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')