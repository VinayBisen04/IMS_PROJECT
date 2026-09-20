from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.auth.authcontroller import login_user
from app.auth.dtos import LoginSchema

router = APIRouter(prefix="/auth")


@router.post("/login/admin")
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return {"access_token": login_user(body, db)}


@router.post("/login/student")
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return {"access_token": login_user(body, db)}