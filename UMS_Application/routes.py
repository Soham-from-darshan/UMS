import base64
from io import BytesIO
import bcrypt
from flask import redirect, render_template, request, url_for, Blueprint
from jinja2 import Undefined
from UMS_Application.models import Faculty, Student, User
from UMS_Application.forms import CreateFacultyForm, CreateStudentForm, CreateUserForm
from UMS_Application import app, db
import base64
from jinja2 import Undefined

#   <form class="d-flex" style="margin-left: 60px;" role="search" method="post">
#                     <input  onchange="{{ url_for('admin.search_students') }}" class="form-control me-2" type="search"
#                         aria-label="Search" name="search_text">
#                     <button class="btn btn-outline-success" style="height: 40px;" type="submit">Search</button>
#                 </form>


bp = Blueprint('admin',__name__,url_prefix='/admin')

from flask import render_template, request

@bp.route('/search_students', methods=['POST'])
def search_students():
    search_text = request.form.get('search_text').lower()
    students = Student.query.filter(
        (Student.EnrollmentNo.ilike(f'%{search_text}%')) |
        (Student.Gmail.ilike(f'%{search_text}%'))
    ).all()
    return render_template('sem_wise_student.html', students=students)

@bp.route('/')
def home():
       return render_template('admin_panel.html')



@bp.route('/student')
def student():
    return render_template('cards.html')


@bp.route('/sem/<int:sem_id>')
def sem_detail(sem_id):
    students = Student.query.filter_by(Sam=sem_id).all()
    return render_template('sem_wise_student.html', students=students)


@bp.route('/delete_student/<int:enrollment_no>', methods=['GET', 'POST'])
def delete_student(enrollment_no):
    
    student_to_delete = Student.query.filter_by(
        EnrollmentNo=enrollment_no).first()
    sem_id = student_to_delete.Sam
    user_id = student_to_delete.UserId
    db.session.delete(student_to_delete)
    db.session.commit()

    user_to_delete = User.query.filter_by(
        UserId=user_id).first()
    db.session.delete(user_to_delete)
    db.session.commit()
    

    return redirect(url_for('admin.sem_detail', sem_id=sem_id))


@bp.route('/add/user', methods=['GET', 'POST'])
def add_user():

    form = CreateUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            password = form.password.data.encode('utf-8')
            hashed_password = bcrypt.hashpw(
                password, bcrypt.gensalt()).decode('utf-8')
            new_user = User(Type=form.type.data,
                            Email=form.email.data, Password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(Email=form.email.data).first()
            form.type.data = form.type.data.lower()
            if form.type.data == 'student':
                return redirect(url_for('admin.add_student', user_id=user.UserId, Gmail=user.Email))
            # if form.type.data == 'faculty':
            else:
                return redirect(url_for('admin.add_faculty', user_id=user.UserId, Gmail=user.Email))
        
        #      return f"{form.errors}"
    
    return render_template('user_form.html', form=form)


@bp.route('/add/student/<int:user_id>/<string:Gmail>', methods=['GET', 'POST'])
def add_student(user_id, Gmail):

    form = CreateStudentForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            new_student = Student(
                Sam=form.sam.data,
                Name=form.name.data,
                Birthdate=form.birthdate.data,
                City=form.city.data,
                Income=form.income.data,
                MobileNo=form.mobile_no.data,
                Gmail=Gmail,
                FeesStatus=form.fees_status.data,
                HSC_pr=form.hsc_pr.data,
                SSC_pr=form.ssc_pr.data,
                Course=form.course.data,
                Branch=form.branch.data,
                Type='student',
                Class=form.class_.data,
                Batch=form.batch.data,
                RollNo=form.roll_no.data,
                EnrollmentNo=form.enrollment_no.data
            )

            if form.image.data and hasattr(form.image.data, 'read'):
                try:
                    # print("Image is obtained by the user - stage-1")
                    new_student.Image = update_image(form.image.data)
                except ValueError as e:
                    # print("Error updating image - stage-2")
                    return f"Error updating image: {str(e)}"
            else:
                # print("Image is not obtained by the user - stage-3")
                return f"{form.image.errors}"

            new_student.UserId = user_id
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('admin.sem_detail', sem_id=new_student.Sam))

        else:
            f"{form.errors}"

    return render_template('student_detail.html', form=form)

    # return render_template('student_detail.html', form=form)


def update_image(file_data):
    try:
        # Ensure that file_data is a file-like object
        if hasattr(file_data, 'read'):
            # Convert the image file to BLOB
            img_bytes_io = BytesIO(file_data.read())
            return img_bytes_io.getvalue()
        else:
            raise ValueError("Invalid file data")
    except Exception as e:
        # Handle other potential errors, like invalid image format, etc.
        raise ValueError(f"Error processing image: {str(e)}")


@bp.route('/edit_student/<int:enrollment_no>', methods=['GET', 'POST'])
def edit_student(enrollment_no):

    student = Student.query.filter_by(EnrollmentNo=enrollment_no).first()
    user_id = student.UserId
    image_file = student.Image
    enrollment_no = student.EnrollmentNo

    form = CreateStudentForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            student.UserId = form.user_id.data
            student.EnrollmentNo = form.enrollment_no.data
            student.Sam = form.sam.data
            student.Name = form.name.data
            student.Birthdate = form.birthdate.data
            student.City = form.city.data
            student.Income = form.income.data
            student.MobileNo = form.mobile_no.data
            student.Gmail = form.gmail.data
            student.FeesStatus = form.fees_status.data
            student.HSC_pr = form.hsc_pr.data
            student.SSC_pr = form.ssc_pr.data
            student.Course = form.course.data
            student.Branch = form.branch.data
            student.Class = form.class_.data
            student.Batch = form.batch.data
            student.RollNo = form.roll_no.data

            # print(form.image.data)
            if form.image.data:
                if form.image.data and hasattr(form.image.data, 'read'):
                    try:
                        print("image is get by user stage-1")
                        student.Image = update_image(form.image.data)
                    except ValueError as e:
                        print("image is get by user  stage-2")

                        return f"Error updating image: {str(e)}"
                else:
                    print("image is not get by user  stage-3")
                    return f"{form.image.errors} "

            else:
                if image_file and hasattr(image_file, 'read'):
                    print("image is get by user stage-1")
                    student.Image = update_image(image_file)

            db.session.commit()
            return redirect(url_for('admin.sem_detail', sem_id=form.sam.data))

        # else:

        #     return f"{form.errors}"

    form.user_id.data = student.UserId
    form.enrollment_no.data = student.EnrollmentNo
    form.sam.data = student.Sam
    form.name.data = student.Name
    form.birthdate.data = student.Birthdate
    form.city.data = student.City
    form.income.data = student.Income
    form.mobile_no.data = student.MobileNo
    form.gmail.data = student.Gmail
    form.fees_status.data = student.FeesStatus
    form.hsc_pr.data = student.HSC_pr
    form.ssc_pr.data = student.SSC_pr
    form.course.data = student.Course
    form.branch.data = student.Branch
    form.class_.data = student.Class
    form.batch.data = student.Batch
    form.roll_no.data = student.RollNo
    form.image.data = student.Image

    return render_template('student_detail.html', form=form)


# @bp.route('/debug_image/<int:enrollment_no>')
# def debug_image(enrollment_no):
#     student = Student.query.filter_by(EnrollmentNo=enrollment_no).first()
#     return str(student.Image)


@bp.route('/search_faculty', methods=['POST','GET'])
def search_faculty():
    search_text = request.form.get('search_text').lower()
    faculties = Faculty.query.filter(
        (Faculty.FacultyId.ilike(f'%{search_text}%')) |
        (Faculty.Gmail.ilike(f'%{search_text}%'))
    ).all()
    
    return render_template('department_wise_faculty.html', facultys=faculties)

@bp.route('/faculty')
def faculty():

    form = CreateFacultyForm()
    facultys = Faculty.query.all()
    return render_template('department_wise_faculty.html', facultys=facultys, form=form)


@bp.route('/edit_faculty/<int:faculty_id>', methods=['GET', 'POST'])
def edit_faculty(faculty_id):
    faculty = Faculty.query.filter_by(FacultyId=faculty_id).first()
    image_file = faculty.Image
    email_id = faculty.Gmail
    form = CreateFacultyForm()

    if request.method == 'POST':
        print(faculty, "before the form.validate_on_submit() ")

        if form.validate_on_submit():
            faculty.UserId = form.user_id.data
            faculty.FacultyId = form.faculty_id.data
            faculty.Name = form.name.data
            faculty.MobileNo = form.mobile_no.data
            faculty.Gmail = form.gmail.data
            faculty.Course = form.course.data
            faculty.Experience = form.experience.data
            faculty.Cabin = form.cabin.data
            faculty.Department = form.department.data
            faculty.Course = form.course.data

            print(faculty, "inside the form.validate_on_submit()")
            # print(faculty.Image)
            if form.image.data:
                if form.image.data and hasattr(form.image.data, 'read'):
                    try:    
                        print("image is get by user stage-1")
                        faculty.Image = update_image(form.image.data)
                    except ValueError as e:
                        print("image is get by user stage-2")
                        return f"Error updating image: {str(e)}"
                else:
                    print("image is not get by user stage-3")
                    return f"{form.image.errors}"
            else:
                if image_file and hasattr(image_file, 'read'):
                    print("image is get by user stage-1")
                    faculty.Image = update_image(image_file)

            db.session.commit()
            #   flash('The account has been updated!', 'success')
            return redirect(url_for('admin.faculty'))

        # else:
        #     return f"{form.errors}"

    form.user_id.data = faculty.UserId
    form.faculty_id.data = faculty_id
    form.name.data = faculty.Name
    form.mobile_no.data = faculty.MobileNo
    form.gmail.data = faculty.Gmail
    form.course.data = faculty.Course
    form.experience.data = faculty.Experience
    form.cabin.data = faculty.Cabin
    form.department.data = faculty.Department
    form.image.data = faculty.Image

    return render_template('faculty_detail.html', form=form)


@bp.route('/add_faculty/<int:user_id>/<string:Gmail>', methods=['GET', 'POST'])
def add_faculty(user_id, Gmail):
    form = CreateFacultyForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_faculty = Faculty(
                # FacultyId=form.faculty_id.data,
                Name=form.name.data,
                MobileNo=form.mobile_no.data,
                Gmail=form.gmail.data,
                Course=form.course.data,
                Experience=form.experience.data,
                Cabin=form.cabin.data,
                Department=form.department.data
            )

            if form.image.data and hasattr(form.image.data, 'read'):
                try:
                    new_faculty.Image = update_image(form.image.data)
                except ValueError as e:
                    return f"Error updating image: {str(e)}"
            else:
                return f"{form.image.errors}"

            new_faculty.UserId = user_id
            db.session.add(new_faculty)
            db.session.commit()

            # Redirect to a different route upon successful submission
            return redirect(url_for('admin.faculty'))

    # else:
    #     # Add a missing return statement here
    #     return f"{form.errors}"

    return render_template('faculty_detail.html', form=form)


@bp.route('/delete_faculty/<int:faculty_id>')
def delete_faculty(faculty_id):

    faculty_to_delete = Faculty.query.filter_by(FacultyId=faculty_id).first()
    user_id = faculty_to_delete.UserId
    db.session.delete(faculty_to_delete)
    db.session.commit()
    
    user_to_delete = User.query.filter_by(
        UserId=user_id).first()
    db.session.delete(user_to_delete)
    db.session.commit()

    return redirect(url_for('admin.faculty'))


@bp.app_template_filter('b64encode')
def b64encode_filter(s):
    # Check if s is of type 'Undefined'
    if isinstance(s, Undefined):
        return s

    try:
        # Encode the data
        encoded_data = base64.b64encode(s).decode('utf-8')

        # Debugging: Print encoded data
        # print(f"Encoded Data: {encoded_data}")

        # Return the encoded data
        return encoded_data
    except Exception as e:
        # Handle any errors that might occur during encoding
        print(f"Error encoding data: {str(e)}")
        return f"Error encoding data: {str(e)}"
