import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from repositories.employment_details_repo import create_employment_details
from core.security import create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from core.password import hash_password, verify_password
from models.models import EmploymentDetails
from schemas.employment_details_schema import EmploymentCreate
from database import get_db
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt

router = APIRouter(prefix="/employment_details", tags=["Employment Details"])





@router.post("/employment_details")
def create_employment_detail(employment: EmploymentCreate, db: Session = Depends(get_db)):
    return create_employment_details(db, employment)


@router.delete("/employment_details/{employment_id}")
def delete_employment_details(employment_id: uuid.UUID, db: Session = Depends(get_db    )):
    employment = db.query(EmploymentDetails).filter(EmploymentDetails.employment_details_id == employment_id).first()
    if not employment:
        raise HTTPException(status_code=404, detail="Employment details not found")
    db.delete(employment)
    db.commit()
    return {"message": "Employment details deleted successfully"}   

@router.patch("/employment_details/{employment_id}")
def update_employment_details(employment_id: uuid.UUID, employment_update: EmploymentCreate, db = Depends(get_db)):
    employment = db.query(EmploymentDetails).filter(EmploymentDetails.employment_details_id == employment_id).first()
    if not employment:
        raise HTTPException(status_code=404, detail="Employment details not found")
    employment.employer_first_name = employment_update.employer_first_name
    employment.employer_last_name = employment_update.employer_last_name
    employment.job_title = employment_update.job_title
    employment.monthly_income = employment_update.monthly_income
    employment.employment_type = employment_update.employment_type
    db.commit()
    db.refresh(employment)
    return employment   

@router.get("/employment_details/{employment_id}")
def get_employment_details(employment_id: uuid.UUID, db: Session = Depends(get_db)):
    employment = db.query(EmploymentDetails).filter(EmploymentDetails.employment_details_id == employment_id).first()
    if not employment:
        raise HTTPException(status_code=404, detail="Employment details not found")
    return employment