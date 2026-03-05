from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from repositories.savings_account_repo import create_savings_account_repo
from core.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from models.models import EmploymentDetails
from schemas.savings_account_schema import SavingsAccountCreate
from database import get_db
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt

router = APIRouter(prefix="/savings_account", tags=["Savings_account"])



@router.post("/create")
def create_savings_account(
    account: SavingsAccountCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return create_savings_account_repo(db, account)