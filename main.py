import os
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from app.ims.router import router as ims_router
from app.auth.router import router as auth_router
from app.utils.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Institute Management System")

@app.get("/")
def root():
    return {
        "message": "Institute Management System API is running",
        "docs": "/docs"
    }

app.include_router(auth_router)
app.include_router(ims_router)