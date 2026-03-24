from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
from typing import List
from database import get_db
from models.models import Admin, SavingsAccount, Customer
from schemas.admin_schema import AdminCreate, SavingAccountAdmin
from repositories.admin_repo import create_admin, get_admin_unverified_savings_accounts
from core.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM
import uuid
id=7

def get_all_unverifed_accounts(self, admin_id):
    get_admin_unverified_savings_accounts(db=Depends(get_db), admin_id=admin_id)