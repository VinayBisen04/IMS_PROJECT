from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.ims.models import Teacher, Course, Enrollment, Admin, Batch, Student
from app.ims.dtos import TeacherCreate, CourseCreate, FeeUpdate, AdminCreate, TeacherUpsert, BatchCreate, BatchTeacherUpdate, AssignBatchToEnrollment, BatchAssignTeacher , AdminUpdate, StudentUpdate

#--------Admin
def create_admin(body: AdminCreate, db: Session):
    existing = db.query(Admin).filter(Admin.email == body.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")

    admin = Admin(
        email=body.email,
        password=body.password,
        role="ADMIN"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

def get_admin(admin_id: int, db: Session):
    admin = db.query(Admin).get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

def get_all_admins(db: Session):
    return db.query(Admin).all()

def update_admin(admin_id: int, data: AdminUpdate, db: Session):
    admin = db.query(Admin).get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(admin, key, value)

    db.commit()
    return admin

def delete_admin(admin_id: int, db: Session):
    admin = db.query(Admin).get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted"}

#-------Student
def get_all_students(db: Session):
    return db.query(Student).all()

def get_student(student_id: int, db: Session):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def update_student(student_id: int, data: StudentUpdate, db: Session):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(student, key, value)

    db.commit()
    return student

def delete_student(student_id: int, db: Session):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted"}

#-------Teacher
def create_teacher(body:TeacherCreate, db: Session):
    teacher = Teacher(**body.model_dump())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher

#-----------Course
def create_course(body: CourseCreate, db: Session):
    course = Course(**body.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def get_all_courses(db):
    return db.query(Course).all()

def get_course(course_id: int, db):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(404, "Course not found")
    return course

def update_course(course_id: int, data, db):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(404, "Course not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(course, k, v)

    db.commit()
    return course

def delete_course(course_id: int, db):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(404, "Course not found")

    db.delete(course)
    db.commit()
    return {"message": "Course deleted"}

#---------Fee
def update_fee(enrollment_id: int, body: FeeUpdate, db: Session):
    enrollment = db.query(Enrollment).get(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    enrollment.fee_status = body.fee_status
    db.commit()
    return {"message": "Fee status updated"}


#---------BATCH
def create_batch(body:BatchCreate, db: Session):
    course = db.query(course).get(body.course_id)
    if not course:
        raise HTTPException(status_code=404, detail= "Course not found")
    
    batch = Batch(name = body.name, course_id = body.course_id)
    db.add(Batch)
    db.commit()
    db.refresh(batch)
    return Batch

def get_all_batches(db):
    return db.query(Batch).all()


def get_batch(batch_id: int, db):
    batch = db.query(Batch).get(batch_id)
    if not batch:
        raise HTTPException(404, "Batch not found")
    return batch


def update_batch(batch_id: int, data: BatchAssignTeacher, db):
    batch = db.query(Batch).get(batch_id)
    if not batch:
        raise HTTPException(404, "Batch not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(batch, k, v)

    db.commit()
    return batch


def delete_batch(batch_id: int, db):
    batch = db.query(Batch).get(batch_id)
    if not batch:
        raise HTTPException(404, "Batch not found")

    db.delete(batch)
    db.commit()
    return {"message": "Batch deleted"}


def update_batch_teacher(batch_id:int, body:BatchTeacherUpdate, db:Session):
    batch = db.query(Batch).get(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if body.teacher_id:
        teacher = db.query(Teacher).get(body.teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        batch.teacher_id = body.teacher_id
    else:
        batch.teacher_id = None

    db.commit()
    return {"message": "Batch teacher updated"}

def assign_batch_to_enrollment(enrollment_id: int, body: AssignBatchToEnrollment, db: Session):
    enrollment = db.query(Enrollment).get(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    batch = db.query(Batch).get(body.batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    if enrollment.course_id != batch.course_id:
        raise HTTPException(
            status_code=400,
            detail="Batch does not belong to the enrolled course"
        )

    enrollment.batch_id = body.batch_id
    db.commit()

    return {"message": "Batch assigned to enrollment"}

#-----------upsert teacher
def get_all_teachers(db):
    return db.query(Teacher).all()


def get_teacher(teacher_id: int, db):
    teacher = db.query(Teacher).get(teacher_id)
    if not teacher:
        raise HTTPException(404, "Teacher not found")
    return teacher


def update_teacher(teacher_id: int, data, db):
    teacher = db.query(Teacher).get(teacher_id)
    if not teacher:
        raise HTTPException(404, "Teacher not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(teacher, k, v)

    db.commit()
    return teacher


def delete_teacher(teacher_id: int, db):
    teacher = db.query(Teacher).get(teacher_id)
    if not teacher:
        raise HTTPException(404, "Teacher not found")

    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted"}

def upsert_teacher(body:TeacherUpsert, db:Session):
    if body.teacher_id:
        teacher = db.query(Teacher).filter(Teacher.id == body.teacher_id).first()
    
        if teacher:
            teacher.name = body.name
            teacher.email = body.email
            teacher.qualification = body.qualification

            db.commit()
            db.refresh(teacher)

            return{
                    "message": "Teacher updated successfully",
                    "teacher_id": teacher.id
                }
        
    teacher = Teacher(
        name=body.name,
        email=body.email,
        qualification=body.qualification
    )

    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    return {
        "message": "Teacher created successfully",
        "teacher_id": teacher.id
    }

