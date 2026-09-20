from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.ims import controller, admincontroller, dtos
from app.utils.helper import admin_only
from app.ims.dtos import AIQueryRequest
from app.ims.controller import ai_query_controller
router = APIRouter(prefix="/ims")


@router.post("/admin/create")
def create_admin(data: dtos.AdminCreate, db: Session = Depends(get_db)):
    return admincontroller.create_admin(data, db)



@router.post("/students")
async def register_student(body: dtos.StudentCreate, db: Session = Depends(get_db)):
    return await controller.create_student(body, db)


@router.post("/enroll/{student_id}")
def enroll(student_id: int, body: dtos.EnrollmentCreate, db: Session = Depends(get_db)):
    return controller.enroll_course(student_id, body, db)


@router.post("/admin/teacher",dependencies=[Depends(admin_only)])
def add_teacher(body: dtos.TeacherCreate, db: Session = Depends(get_db)):
    return admincontroller.create_teacher(body, db)


@router.post("/admin/course")
def add_course(body: dtos.CourseCreate, db: Session = Depends(get_db)):
    return admincontroller.create_course(body, db)



@router.put("/admin/fee/{enrollment_id}")
def update_fee(enrollment_id: int, body: dtos.FeeUpdate, db: Session = Depends(get_db)):
    return admincontroller.update_fee(enrollment_id, body, db)

@router.post("/teacher/upsert", dependencies=[Depends(admin_only)])
def upsert_teacher_api(body:dtos.TeacherUpsert, db:Session=Depends(get_db)):
    return admincontroller.upsert_teacher(body,db)

@router.post("/batch")
def create_batch_api(body: dtos.BatchCreate,db: Session = Depends(get_db),
    admin=Depends(admin_only)):
    return admincontroller.create_batch(body, db)

@router.put("/batch/{batch_id}/teacher")
def update_teacher_api(batch_id: int,body: dtos.BatchAssignTeacher,db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.update_batch_teacher(batch_id, db)


@router.put("/enrollment/{enrollment_id}/batch")
def assign_batch_api(enrollment_id: int,body: dtos.BatchAssignTeacher,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.assign_batch_to_enrollment(enrollment_id, body, db)

#------new
@router.get("/courses")
def courses(db=Depends(get_db), admin=Depends(admin_only)):
    return admincontroller.get_all_courses(db)


@router.get("/course/{id}")
def course(id: int, db=Depends(get_db), admin=Depends(admin_only)):
    return admincontroller.get_course(id, db)


@router.put("/course/{id}")
def update_course(id: int, body: dtos.CourseUpdate, db=Depends(get_db), admin=Depends(admin_only)):
    return admincontroller.update_course(id, body, db)


@router.delete("/course/{id}")
def delete_course(id: int, db=Depends(get_db), admin=Depends(admin_only)):
    return admincontroller.delete_course(id, db)


#-----------new

@router.get("/admins")
def get_admins(
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.get_all_admins(db)


@router.get("/admin/{admin_id}")
def get_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.get_admin(admin_id, db)


@router.put("/admin/{admin_id}")
def update_admin(
    admin_id: int,
    body: dtos.AdminUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.update_admin(admin_id, body, db)


@router.delete("/admin/{admin_id}")
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.delete_admin(admin_id, db)


@router.get("/students")
def get_students(
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.get_all_students(db)


@router.get("/student/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.get_student(student_id, db)


@router.put("/student/{student_id}")
def update_student(
    student_id: int,
    body: dtos.StudentUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.update_student(student_id, body, db)


@router.delete("/student/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return admincontroller.delete_student(student_id, db)

@router.post("/ai-query")
def ai_query(payload: AIQueryRequest, db: Session = Depends(get_db)):
    answer = ai_query_controller(payload.question, db)
    return {"answer": answer}
