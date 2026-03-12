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

router = APIRouter(prefix="/customer", tags=["Customer"])





@router.post("/employment_details")
def create_employment_details(employment: EmploymentCreate, db: Session = Depends(get_current_user)):
    return create_employment_details(db, employment)
