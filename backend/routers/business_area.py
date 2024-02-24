from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.database import get_session
from db.db_businessarea import (
    create,
    get_all,
    delete_,
    get_all_existing,
    get_all_area_questions,
)
from db.models import BusinessAreaCreate, BusinessAreaRead, QuestionRead


router = APIRouter(
    prefix="/businessarea",
    tags=["businessarea"],
)


@router.post("/{business_type_id}", response_model=BusinessAreaRead)
def create_business_area(business_area: BusinessAreaCreate, session: Session = Depends(get_session)):
    return create(session=session, business_area=business_area)


@router.get("/{business_type_id}", response_model=list[BusinessAreaRead])
def get_all_business_areas(business_type_id: str, session: Session = Depends(get_session)):
    return get_all(session=session, business_type_id=business_type_id)


@router.get("", response_model=list[BusinessAreaRead])
def get_all_existing_business_areas(session: Session = Depends(get_session)):
    return get_all_existing(session=session)


@router.delete("/{business_area_id}")
def delete_businesstype(business_area_id: str, session: Session = Depends(get_session)):
    return delete_(session=session, business_area_id=business_area_id)


@router.get("/{business_area_id}/questions", response_model=list[QuestionRead])
def get_business_area_questions(business_area_id: str, session: Session = Depends(get_session)):
    return get_all_area_questions(session=session, business_area_id=business_area_id)
