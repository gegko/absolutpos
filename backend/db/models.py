from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4


class BusinessBase(SQLModel):
    name: str
    city: str
    address: str


class BusinessCreate(BusinessBase):
    pass


class BusinessRead(BusinessBase):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class BusinessUpdate(SQLModel):
    name: str | None
    city: str | None
    address: str | None
    businesstype_id: str | None
    businessarea_id: str | None


class Business(BusinessBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    businesstype_id: UUID | None = Field(default=None, foreign_key="businesstype.id")
    businessarea_id: UUID | None = Field(default=None, foreign_key="businessarea.id")

    businesstype: Optional["BusinessType"] = Relationship(back_populates="businesses")
    businessarea: Optional["BusinessArea"] = Relationship(back_populates="businesses")
    answers: list["Answer"] | None = Relationship(back_populates="business")


class BusinessTypeBase(SQLModel):
    name: str


class BusinessTypeCreate(BusinessTypeBase):
    pass


class BusinessTypeRead(BusinessTypeBase):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class BusinessType(BusinessTypeBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    businessareas: list["BusinessArea"] | None = Relationship(back_populates="businesstype")
    businesses: list[Business] | None = Relationship(back_populates="businesstype")


class BusinessAreaQuestionLink(SQLModel, table=True):
    businessarea_id: UUID | None = Field(
        default=None,
        foreign_key="businessarea.id",
        primary_key=True,
    )
    question_id: UUID | None = Field(
        default=None,
        foreign_key="question.id",
        primary_key=True,
    )


class BusinessAreaBase(SQLModel):
    name: str
    businesstype_id: UUID = Field(default=None, foreign_key="businesstype.id")


class BusinessAreaCreate(BusinessAreaBase):
    pass


class BusinessAreaRead(BusinessAreaBase):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    businesses: list[Business] | None = Relationship(back_populates="businessarea")


class BusinessArea(BusinessAreaBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    businesses: list[Business] | None = Relationship(back_populates="businessarea")
    businesstype: BusinessType = Relationship(back_populates="businessareas")
    questions: list["Question"] = Relationship(
        back_populates="businessareas",
        link_model=BusinessAreaQuestionLink,
        sa_relationship_kwargs={"cascade": "delete"},
    )


class QuestionBase(SQLModel):
    text: str


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    businessareas: list[BusinessArea] | None = Relationship(
        back_populates="questions",
        link_model=BusinessAreaQuestionLink,
    )


class QuestionUpdate(QuestionBase):
    businessareas: list[str]


class Question(QuestionBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    businessareas: list[BusinessArea] | None = Relationship(
        back_populates="questions",
        link_model=BusinessAreaQuestionLink,
        sa_relationship_kwargs={"cascade": "delete"},
    )
    # questionsubject: QuestionSubject = Relationship(back_populates="questions")
    answers: list["Answer"] | None = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade": "delete"},
    )


class AnswerBase(SQLModel):
    text: str
    business_id: UUID = Field(default=None, foreign_key="business.id")
    question_id: UUID = Field(default=None, foreign_key="question.id")


class AnswerCreate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    pass


class Answer(AnswerBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    question: Question = Relationship(back_populates="answers")
    business: Optional[Business] = Relationship(back_populates="answers")
