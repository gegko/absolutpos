from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.database import get_session
from db.db_business import create, update_
from db.models import BusinessCreate, BusinessRead, BusinessUpdate


router = APIRouter(
    prefix="/business",
    tags=["business"],
)


@router.post("", response_model=BusinessRead)
def create_business(business: BusinessCreate, session: Session = Depends(get_session)):
    return create(session=session, business=business)


@router.patch("/{business_id}", response_model=BusinessRead)
def update_question(
    business_id: str,
    request: BusinessUpdate,
    session: Session = Depends(get_session),
):
    print(request)
    return update_(
        session=session,
        business_id=business_id,
        business_name=request.name,
        business_city=request.city,
        business_address=request.address,
        business_type_id=request.businesstype_id,
        business_area_id=request.businessarea_id,
    )
