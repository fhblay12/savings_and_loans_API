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
import logging
logger = logging.getLogger(__name__)
from log_conf import init_logging
init_logging()
import uuid
id=7

from decimal import Decimal
def standard_loan_payment(loan, payment_amount: Decimal): 
    print(f"Applying standard loan payment. Original loan amount: {loan.loan_amount}, Payment amount: {payment_amount}, Interest rate: {loan.interest_rate}")
    
    # Apply interest first
    loan.loan_amount *= (Decimal("1.0") + loan.interest_rate)

    # Then subtract payment
    loan.loan_amount -= payment_amount

    return loan.loan_amount