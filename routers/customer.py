from fastapi import APIRouter, Depends, HTTPException, logger, status
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import Request
from database import SessionLocal
from repositories import customer_repo
from schemas.customer_schema import CustomerCreate, CustomerUpdate, LoginRequest, customer_form
from schemas.transaction_schema import Transaction
from schemas.savings_account_schema import SavingsAccountCreate, SavingsAccountResponse
from repositories.customer_repo import create_customer, get_savings_accounts, transaction, get_loans, update_customer, customer_login, get_member_by_id, delete_customer
from services.customer_loan_payment_services import standard_loan_payment
from core.security import create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from core.password import hash_password, verify_password
from models.models import Customer, Transactions, SavingsAccount, Loan, LoanPayment
from database import get_db
from typing import List                                                                                                                                                                                                                                                                                                                                                                                                                             
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
import uuid
from decimal import Decimal
from fastapi.templating import Jinja2Templates
from datetime import datetime
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException, Depends


router = APIRouter(prefix="/customer", tags=["Customer"])

#@router.get("/register", response_class=HTMLResponse)
#def collateral(request: Request):
#    return templates.TemplateResponse(
#        "register.html",
#        {
#            "request": request,
#        }
#    )
@router.post("/register")
def create_registration_endpoint(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        customer=create_customer(db, customer)
        return {
            "message": "User registered successfully",
            "customer": customer
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = customer_login(db, LoginRequest(email=form_data.username, password=form_data.password))    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = create_access_token({"sub": user.email, "id": str(user.customer_id), "type": "customer"})


    return {
    "access_token": token,
    "token_type": "bearer"
}

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.patch("/update/{customer_id}")
def update_customers(customer_id: uuid.UUID, customer: CustomerUpdate, db: Session = Depends(get_db)):
    try:
        updated_customer = update_customer(db=db, customer_id=customer_id, customer_update=customer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return { 
        "message": "Customer updated successfully",
        "customer": updated_customer
    }

@router.delete("/delete/{customer_id}")
def delete_customers(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        delete_customer(db, customer_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Item deleted"}
@router.post("/refresh", response_model=Token)
def refresh_token_endpoint(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub") 
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Issue new access token (optional: new refresh token)
        access_token = create_access_token({"sub": user_id})
        return {"access_token": access_token, "refresh_token": refresh_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

