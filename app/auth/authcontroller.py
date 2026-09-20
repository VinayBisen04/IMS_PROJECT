from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.utils.helper import create_access_token
from app.ims.models import Admin, Student
from app.auth.dtos import LoginSchema


def login_user(data: LoginSchema, db: Session):
    admin = db.query(Admin).filter(Admin.email == data.email).first()
    if admin and admin.password == data.password:
        return create_access_token({"user_id": admin.id, "role": "ADMIN"})

    student = db.query(Student).filter(Student.email == data.email).first()
    if student and student.password == data.password:
        return create_access_token({"user_id": student.id, "role": "STUDENT"})

    raise HTTPException(status_code=401, detail="Invalid credentials")
