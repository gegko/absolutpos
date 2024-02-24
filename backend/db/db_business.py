from fastapi import HTTPException, status
from db.models import Business, BusinessCreate
from sqlmodel import Session, select, update


def create(session: Session, business: BusinessCreate):
    db_business = Business.model_validate(business)
    session.add(db_business)
    session.commit()
    session.refresh(db_business)
    return db_business


def update_(
    session: Session,
    business_id: str,
    business_name: str | None,
    business_city: str | None,
    business_address: str | None,
    business_type_id: str | None,
    business_area_id: str | None,
):
    db_business = session.exec(
        select(Business).where(Business.id == business_id)
    ).first()
    if not db_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Бизнес с id '{db_business}' не найден",
        )
    print(business_name)
    if business_name:
        session.exec(
            update(Business)
            .where(Business.id == business_id)
            .values(name=business_name)
        )
    print(business_city)
    if business_city:
        session.exec(
            update(Business)
            .where(Business.id == business_id)
            .values(city=business_city)
        )
    print(business_address)
    if business_address:
        session.exec(
            update(Business)
            .where(Business.id == business_id)
            .values(address=business_address)
        )
    if business_type_id:
        session.exec(
            update(Business)
            .where(Business.id == business_id)
            .values(businesstype_id=business_type_id)
        )
    if business_area_id:
        session.exec(
            update(Business)
            .where(Business.id == business_id)
            .values(businessarea_id=business_area_id)
        )
    session.commit()
    session.refresh(db_business)
    return db_business
