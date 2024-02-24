from fastapi import HTTPException, status

from db.models import BusinessType, BusinessTypeCreate
from sqlmodel import Session, select, delete


def create(session: Session, business_type: BusinessTypeCreate):
    db_business_type = BusinessType.model_validate(business_type)
    session.add(db_business_type)
    session.commit()
    session.refresh(db_business_type)
    return db_business_type


def get_all(session: Session):
    return session.exec(select(BusinessType)).all()


def delete_(session: Session, business_type_id: str):
    businesstype = session.exec(
        select(BusinessType).where(BusinessType.id == business_type_id)
    ).first()
    if not businesstype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сфера с id '{business_type_id}' не найдена",
        )
    session.exec(delete(BusinessType).where(BusinessType.id == business_type_id))
    session.commit()
    return "OK"
