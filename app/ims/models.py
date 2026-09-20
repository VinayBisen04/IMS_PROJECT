from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.utils.db import Base

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="ADMIN")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="STUDENT")
    
class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    qualification = Column(String, nullable=False)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    fee = Column(Float, nullable=False)

class Batch(Base):
    __tablename__ = "batches"
    id = Column(Integer,primary_key=True)
    name = Column(String, nullable=False)
    course_id = Column(Integer,ForeignKey("courses.id"),nullable=False)
    teacher_id = Column(Integer,ForeignKey("teachers.id"), nullable=True)

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    fee_status = Column(String, default="PENDING")
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=True)


class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True)
    student_email = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    amount = Column(Float)
    status = Column(String)
