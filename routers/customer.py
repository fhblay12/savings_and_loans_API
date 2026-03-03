from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.customer_schema import CustomerCreate
from repositories.customer_repo import create_customer

router = APIRouter(prefix="/customer", tags=["Customer"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_registration_endpoint(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)