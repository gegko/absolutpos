# from db.models import QuestionSubject, QuestionSubjectCreate
# from sqlmodel import Session, select


# def create(session: Session, question_subject: QuestionSubjectCreate):
#     db_question_subject = QuestionSubject.model_validate(question_subject)
#     session.add(db_question_subject)
#     session.commit()
#     session.refresh(db_question_subject)
#     return db_question_subject


# def get_all(session: Session):
#     return session.exec(select(QuestionSubject)).all()
