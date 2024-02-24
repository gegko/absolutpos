from fastapi import HTTPException, status
from db.models import BusinessArea, BusinessAreaCreate
from sqlmodel import Session, select, delete
from uuid import UUID


def create(session: Session, business_area: BusinessAreaCreate):
    db_business_area = BusinessArea.model_validate(business_area)
    session.add(db_business_area)
    session.commit()
    session.refresh(db_business_area)
    return db_business_area


def get_all(session: Session, business_type_id: UUID):
    return session.exec(
        select(BusinessArea)
        .where(BusinessArea.businesstype_id == business_type_id)
    ).all()


def get_all_existing(session: Session):
    return session.exec(
        select(BusinessArea)
    ).all()


def delete_(session: Session, business_area_id: str):
    businessarea = session.exec(
        select(BusinessArea).where(BusinessArea.id == business_area_id)
    ).first()
    if not businessarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Направление с id '{business_area_id}' не найдено",
        )
    session.exec(delete(BusinessArea).where(BusinessArea.id == business_area_id))
    session.commit()
    return "OK"


def get_all_area_questions(session: Session, business_area_id: str):
    print("here88888888888888888888888888")
    area = session.exec(
        select(BusinessArea)
        .where(BusinessArea.id == business_area_id)
    ).first()
    questions = area.questions
    print(area)
    print(questions)
    if not questions:
        return []
    return questions
