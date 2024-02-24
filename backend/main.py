from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import init_db
from routers import answer, business, business_area, business_type, question, question_subject


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(answer.router)
app.include_router(business_area.router)
app.include_router(business_type.router)
app.include_router(business.router)
# app.include_router(question_subject.router)
app.include_router(question.router)


origins = [
    "http://localhost:3000",
    "http://localhost:5000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
