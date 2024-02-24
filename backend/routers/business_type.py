from fastapi import APIRouter, Depends
from sqlmodel import Session, delete

from db.database import get_session
from db.db_businesstype import create, get_all, delete_
from db.models import BusinessTypeCreate, BusinessTypeRead


router = APIRouter(
    prefix="/businesstype",
    tags=["businesstype"],
)


@router.post("", response_model=BusinessTypeRead)
def create_business_type(business_type: BusinessTypeCreate, session: Session = Depends(get_session)):
    return create(session=session, business_type=business_type)


@router.get("", response_model=list[BusinessTypeRead])
def get_all_business_types(session: Session = Depends(get_session)):
    return get_all(session=session)


@router.delete("/{business_type_id}")
def delete_businesstype(business_type_id: str, session: Session = Depends(get_session)):
    return delete_(session=session, business_type_id=business_type_id)
