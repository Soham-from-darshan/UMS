from flask_login import UserMixin
import sqlalchemy
from UMS_Application import db
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey, UniqueConstraint, CheckConstraint, BLOB
from sqlalchemy.orm import declarative_base, relationship



class User(db.Model, UserMixin):

    __tablename__ = 'User'

    UserId = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Type = Column(Text, nullable=False)
    Email = Column(Text, unique=True, nullable=False)
    Password = Column(Text, nullable=False)

    def get_id(self):
        print(str(self.UserId))
        return str(self.UserId)

    def __repr__(self):
        return f"User('{self.Email}', '{self.Type}', '{self.Password}')"




class Student(db.Model, UserMixin):
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

    def get_id(self):
        return str(self.UserId)

class Faculty(db.Model, UserMixin):
    __tablename__ = 'Faculty'
    
    FacultyId = Column(Integer, primary_key=True, nullable=False)
    UserId = Column(Integer, ForeignKey('User.UserId'), nullable=False)
    Type = Column(Text, nullable=False)
    Name = Column(Text, nullable=False)
    MobileNo = Column(Integer, nullable=False)
    Gmail = Column(Text, nullable=False)
    Experience = Column(Integer, nullable=False)
    Cabin = Column(Text)
    Department = Column(Text, nullable=False)
    Course = Column(Text, nullable=False)
    Image = Column(BLOB, nullable=False)
    
    def get_id(self):
        return str(self.UserId)

class Subject(db.Model):
    __tablename__ = 'Subject'

    SubCode = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(Text, nullable=False)
    Sam = Column(Integer,nullable=False)
    Image = Column(BLOB,nullable=False)

class FacultySubject(db.Model):
    __tablename__ = 'FacultySubject'

    Id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    FacId = Column(Integer, ForeignKey('User.UserId'), nullable=False)
    SubId = Column(Text, ForeignKey('Subject.SubCode'), nullable=False)

class SubjectFile(db.Model):
    __tablename__ = 'SubjectFile'

    Id = Column(Integer, primary_key=True, nullable=False)
    SubCode = Column(Text, ForeignKey('Subject.SubCode'), nullable=False)
    Filedata = Column(BLOB, nullable=False)
    Name = Column(Text,nullable=False)

if __name__ == '__main__':
    db.create_all()