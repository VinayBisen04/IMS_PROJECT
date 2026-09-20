from pydantic import BaseModel
from typing import Optional

#------admin
class AdminCreate(BaseModel):
    email: str
    password: str

class AdminUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

class StudentCreate(BaseModel):
    name: str
    email: str
    password: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class TeacherCreate(BaseModel):
    name: str
    email: str
    qualification: str

#------Course
class CourseCreate(BaseModel):
    title: str
    fee: float
    teacher_id: int

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    fee: Optional[float] = None


class EnrollmentCreate(BaseModel):
    course_id: int

class FeeUpdate(BaseModel):
    fee_status: str

class TeacherUpsert(BaseModel):
    teacher_id: Optional[int] = None
    name: str
    email: str
    qualification: str


class BatchCreate(BaseModel):
    name: str
    course_id: int


class BatchTeacherUpdate(BaseModel):
    teacher_id: Optional[int] = None


class AssignBatchToEnrollment(BaseModel):
    batch_id: int

class BatchAssignTeacher(BaseModel):
    teacher_id: Optional[int] = None

class AIQueryRequest(BaseModel):
    question: str