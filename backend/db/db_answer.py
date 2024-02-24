from db.models import Answer, AnswerCreate
from sqlmodel import Session, select, update


def create(session: Session, answer: AnswerCreate):
    db_answer = Answer.model_validate(answer)
    session.add(db_answer)
    session.commit()
    session.refresh(db_answer)
    return db_answer


def answer_exists(session: Session, answer: AnswerCreate):
    business_id = answer.business_id
    question_id = answer.question_id
    db_answer = session.exec(
        select(Answer)
        .where(Answer.business_id == business_id, Answer.question_id == question_id)
    ).first()
    if not db_answer:
        return False
    return True


def update_(session: Session, answer: AnswerCreate):
    business_id = answer.business_id
    question_id = answer.question_id
    session.exec(
        update(Answer)
        .where(Answer.business_id == business_id, Answer.question_id == question_id)
        .values(text=answer.text)
    )
    session.commit()
    db_answer = session.exec(
        select(Answer)
        .where(Answer.business_id == business_id, Answer.question_id == question_id)
    ).first()
    return db_answer
