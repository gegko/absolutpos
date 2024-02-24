from fastapi import HTTPException, status
from db.models import Question, QuestionCreate, BusinessArea, BusinessAreaQuestionLink
from sqlmodel import Session, select, update, delete
from uuid import UUID


def create(session: Session, question: QuestionCreate):
    db_question = Question.model_validate(question)
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question


def get_all(session: Session, business_areas: list[str] | None):
    return 
    return session.exec(
        select(Question)
        .where(Question.questionsubject_id == question_subject_id)
    ).all()


def update_(
    session: Session,
    question_id: str,
    question_text: str | None,
    business_areas: list[str] | None,
):
    print(question_id)
    db_question = session.exec(select(Question).where(Question.id == question_id)).first()
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вопрос с id '{question_id}' не найден",
        )
    print(question_text)
    if question_text:
        session.exec(
            update(Question)
            .where(Question.id == question_id)
            .values(text=question_text)
        )
    print(business_areas)
    print('*' * 10)
    if business_areas:
        business_area_list = []
        for area_id in business_areas:
            db_area = session.exec(
                select(BusinessArea)
                .where(BusinessArea.id == area_id)
            ).first()
            if db_area:
                business_area_list.append(db_area)
        db_question.businessareas = business_area_list
    session.commit()
    session.refresh(db_question)
    return db_question


def delete_(session: Session, question_id: str):
    question = session.exec(
        select(Question).where(Question.id == question_id)
    ).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вопрос с id '{question_id}' не найден",
        )
    session.exec(
        delete(BusinessAreaQuestionLink)
        .where(BusinessAreaQuestionLink.question_id == question_id)
    )
    session.exec(delete(Question).where(Question.id == question_id))
    session.commit()
    return "OK"


def get_all_question_areas(session: Session, question_id: str):
    question = session.exec(
        select(Question).where(Question.id == question_id)
    ).first()
    areas = question.businessareas
    if not areas:
        return []
    return areas
