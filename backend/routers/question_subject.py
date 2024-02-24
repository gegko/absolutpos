# from fastapi import APIRouter, Depends
# from sqlmodel import Session

# from db.database import get_session
# from db.db_questionsubject import create
# from db.models import QuestionSubjectCreate, QuestionSubjectRead


# router = APIRouter(
#     prefix="/questionsubject",
#     tags=["questionsubject"],
# )


# @router.post("", response_model=QuestionSubjectRead)
# def create_question_subject(question_subject: QuestionSubjectCreate, session: Session = Depends(get_session)):
#     return create(session=session, question_subject=question_subject)
