import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy.orm import Session

from app.ims import models, dtos
from app.ims.models import Student, Teacher, Fee
from app.utils.mail import send_email

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")


async def create_student(body: dtos.StudentCreate, db: Session):
    student = models.Student(**body.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)

    res = await send_email([student.email])
    print(res)
    return student


def enroll_course(student_id: int, body: dtos.EnrollmentCreate, db: Session):
    enrollment = models.Enrollment(student_id=student_id,course_id=body.course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def ai_query_controller(question: str, db: Session):
    docs = []

    # ---- Students ----
    students = db.query(Student).all()
    for s in students:
        docs.append(f"Student {s.name} is enrolled in {s.course}")

    # ---- Fees ----

    fees = db.query(Fee).all()
    for f in fees:
        # Student ID se student name/email fetch karo
        student = db.query(Student).filter(Student.id == f.student_id).first()
        if student:
            docs.append(f"Student {student.name} (email: {student.email}) has fee {f.amount} and status {f.status}")
        else:
            docs.append(f"Fee {f.amount} with status {f.status} for student_id {f.student_id}")


    # ---- Teachers ----
    teachers = db.query(Teacher).all()
    for t in teachers:
        docs.append(
            f"Teacher {t.name} teaches {t.subject}"
        )

    # ---- Embeddings (FREE & LOCAL) ----

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
    vectorstore = FAISS.from_texts(docs, embeddings)


    # ---- Groq LLM ----
    llm = ChatGroq(
        model_name="openai/gpt-oss-20b",
        temperature=0
    )

    relevant_docs = vectorstore.similarity_search(question, k=4)
    context = " ".join([d.page_content for d in relevant_docs])

    response = llm.invoke(
        f"""
        Answer strictly based on the data below.
        If data is not available, say "Data not found".

        Data:
        {context}

        Question:
        {question}
        """
    )

    return response.content