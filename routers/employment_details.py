import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from repositories.employment_details_repo import create_employment_details, update_employment_details, delete_employment_details, get_member_by_id
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
    try:        
        employment = create_employment_details(db, employment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return employment


@router.delete("/employment_details/{employment_id}")
def delete_employment_details(employment_id: uuid.UUID, db: Session = Depends(get_db    )):
    try:
        employment = delete_employment_details(db, employment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Employment details deleted successfully"}   

@router.patch("/employment_details/{employment_id}")
def update_employment_details(employment_id: uuid.UUID, employment_update: EmploymentCreate, db = Depends(get_db)):
    try:
        employment = update_employment_details(db, employment_id, employment_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return employment   

@router.get("/employment_details/{employment_id}")
def get_employment_details(employment_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        employment = get_member_by_id(db, employment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return employment