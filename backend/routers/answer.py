from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.database import get_session
from db.db_answer import create, answer_exists, update_
from db.models import AnswerCreate, AnswerRead


router = APIRouter(
    prefix="/answer",
    tags=["answer"],
)


@router.post("", response_model=AnswerRead)
def create_or_update_answer(answer: AnswerCreate, session: Session = Depends(get_session)):
    if not answer_exists(session=session, answer=answer):
        return create(session=session, answer=answer)
    return update_(session=session, answer=answer)
