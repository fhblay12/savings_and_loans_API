import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from repositories.savings_account_repo import create_savings_account_repo, update_savings_account
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

):
    return create_savings_account_repo(db, account)

@router.get("/{account_id}")
def get_savings_account(account_id: uuid.UUID, db: Session = Depends(get_db)):
    account = db.query(SavingsAccount).filter(SavingsAccount.account_id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Savings account not found")
    return account

@router.patch("/update/{account_id}")
def update_savings_accounts(account_id: uuid.UUID, account_update: SavingsAccountUpdate, db: Session = Depends(get_db)):
    updated_account = update_savings_account(db=db, account_id=account_id, account_update=account_update)
    return updated_account

@router.delete("/delete/{account_id}")
def delete_savings_account(account_id: uuid.UUID, db: Session = Depends(get_db)):  
    account = db.query(SavingsAccount).filter(SavingsAccount.account_id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Savings account not found")
    db.delete(account)
    db.commit()
    return {"message": "Savings account deleted successfully"}