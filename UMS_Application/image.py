from sqlalchemy import create_engine, Column, BLOB, Integer, Text, Float, CheckConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    UserId = Column(Integer, primary_key=True)
    # Add other columns as needed

class Student(Base):
    __tablename__ = 'Student'

    UserId = Column(Integer, ForeignKey('User.UserId'), nullable=False)
    EnrollmentNo = Column(Integer, unique=True, nullable=False)
    StudentId = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Sam = Column(Integer, CheckConstraint('Sam >= 1 AND Sam <= 8'), nullable=False)
    Name = Column(Text, nullable=False)
    Birthdate = Column(Text, nullable=False)
    City = Column(Text, nullable=False)
    Income = Column(Float, nullable=False)
    MobileNo = Column(Integer, nullable=False)
    Gmail = Column(Text, nullable=False)
    FeesStatus = Column(Text, nullable=False)
    Image = Column(BLOB, nullable=False)
    HSC_pr = Column(Float, nullable=False)
    SSC_pr = Column(Float, nullable=False)
    Course = Column(Text, nullable=False)
    Branch = Column(Text, nullable=False)
    Class = Column(Text)
    Batch = Column(Text)
    RollNo = Column(Integer)
    Type = Column(Text, nullable=False)

# Replace 'sqlite:///your_database.db' with the actual path to your SQLite database file
DATABASE_URL = 'sqlite:///your_database.db'

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Example data (replace this with your actual image data and UserId)
image_data = open('default.jpg', 'rb').read()
user_id_to_update = 2

# Check if the record exists, and update the image if it does
existing_student = (
    session.query(Student)
    .filter_by(UserId=user_id_to_update)
    .first()
)

if existing_student:
    existing_student.Image = image_data
    session.commit()
    print("Image updated successfully.")
else:
    print(f"No record found for UserId={user_id_to_update}.")

session.close()
