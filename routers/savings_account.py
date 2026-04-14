import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from repositories.savings_account_repo import create_savings_account_repo, update_savings_account, get_savings_accounts, get_savings_account_by_id, delete_savings_account
from schemas.savings_account_schema import SavingsAccountCreate, SavingsAccountUpdate
from core.security import create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from core.password import hash_password, verify_password
from models.models import EmploymentDetails, SavingsAccount
from schemas.savings_account_schema import SavingsAccountCreate, SavingsAccountUpdate
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
    current_user = Depends(get_current_user)

):
    try:
        return create_savings_account_repo(db, account)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{account_id}")
def get_savings_account(account_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    account = get_savings_account_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Savings account not found")
    return account

@router.patch("/update/{account_id}")
def update_savings_accounts(account_id: uuid.UUID, account_update: SavingsAccountUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    updated_account = update_savings_account(db=db, account_id=account_id, account_update=account_update)
    if not updated_account:
        raise HTTPException(status_code=404, detail="Savings account not found")    
    return updated_account

@router.delete("/delete/{account_id}")
def delete_savings_accounts(account_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):  
    account = delete_savings_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Savings account not found")
    return {"message": "Savings account deleted successfully"}