import os
import db.models as models
from dotenv import load_dotenv, find_dotenv
from sqlmodel import create_engine, SQLModel, Session


load_dotenv(dotenv_path=find_dotenv())
USER, PASSWORD, DB_HOST, DB_NAME = (
    os.getenv("POSTGRES_USER"),
    os.getenv("POSTGRES_PASSWORD"),
    os.getenv("POSTGRES_HOST"),
    os.getenv("POSTGRES_DB"),
)
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(url=DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
