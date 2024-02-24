from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.database import get_session
from db.db_question import create, update_, get_all, delete_, get_all_question_areas
from db.models import QuestionCreate, QuestionRead, BusinessAreaRead, QuestionUpdate


router = APIRouter(
    prefix="/question",
    tags=["question"],
)


@router.post("", response_model=QuestionRead)
def create_question(question: QuestionCreate, session: Session = Depends(get_session)):
    return create(session=session, question=question)


@router.patch("/{question_id}", response_model=QuestionRead)
def update_question(
    question_id: str,
    request: QuestionUpdate,
    session: Session = Depends(get_session),
):
    print(request)
    return update_(
        session=session,
        question_id=question_id,
        question_text=request.text,
        business_areas=request.businessareas,
    )


@router.delete("/{question_id}")
def delete_question(question_id: str, session: Session = Depends(get_session)):
    return delete_(session=session, question_id=question_id)


@router.get("/{question_id}/business_areas", response_model=list[BusinessAreaRead])
def get_business_area_questions(question_id: str, session: Session = Depends(get_session)):
    return get_all_question_areas(session=session, question_id=question_id)
