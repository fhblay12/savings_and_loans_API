from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.loan_schema import LoanCreate
from repositories.loan_repo import create_loan_details
from core.security import create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from core.password import hash_password, verify_password
from models.models import Loan
from database import get_db
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
import uuid

router = APIRouter(prefix="/loan", tags=["loan"])

@router.post("/apply")
def create_registration_endpoint(loan: LoanCreate, db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    return create_loan_details(db, loan)