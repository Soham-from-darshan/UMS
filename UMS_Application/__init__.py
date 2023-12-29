from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()

app.config.from_mapping(
    SECRET_KEY='ums',
    SQLALCHEMY_DATABASE_URI = r'sqlite:///../Database/ums.sqlite',
    ADMIN_EMAIL = "admin@gmail.com",
    ADMIN_PASSWORD = "big_password"
)


login_manager.init_app(app)
db = SQLAlchemy(app)

from . import authentication
app.register_blueprint(authentication.bp)

from . import student_view
app.register_blueprint(student_view.bp)

from . import faculty_view
app.register_blueprint(faculty_view.bp)

from . import file_transmission
app.register_blueprint(file_transmission.bp)

from . import routes
app.register_blueprint(routes.bp)