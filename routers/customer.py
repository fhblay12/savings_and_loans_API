from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.customer_schema import CustomerCreate
from schemas.transaction_schema import Transaction
from schemas.savings_account_schema import SavingsAccountCreate, SavingsAccountResponse
from repositories.customer_repo import create_customer, get_savings_accounts, transaction, get_loans
from services.customer_loan_payment_services import standard_loan_payment
from core.security import create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from core.password import hash_password, verify_password
from models.models import Customer, Transactions, SavingsAccount, Loan, LoanPayment
from schemas.loan_schema import LoanResponse 
from database import get_db
from typing import List                                                                                                                                                                                                                                                                                                                                                                                                                             
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
import uuid
from decimal import Decimal

router = APIRouter(prefix="/customer", tags=["Customer"])

@router.post("/")
def create_registration_endpoint(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(Customer).filter(Customer.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": user.email, "id": str(user.customer_id), "type": "customer"})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

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
    

@router.get("/{customer_id}/savings-account", response_model=List[SavingsAccountResponse])
def get_savings_accounts_for_admin(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    account = get_savings_accounts(db, customer_id)
    if not account:
        raise HTTPException(status_code=404, detail="No savings account found")
    return [account]  # ✅ return a list of ORM instances

@router.get("/{customer_id}/loan", response_model=List[LoanResponse])
def get_loans_for_customer(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    loans = get_loans(db, customer_id)
    if not loans:
        raise HTTPException(status_code=404, detail="No savings account found")
    return loans  # ✅ return a list of ORM instances

@router.post("/{customer_id}/transaction")
def create_transaction(
    account_id: uuid.UUID,
    amount: float,
    tx_type: str,
    db: Session = Depends(get_db)
):

    amount = Decimal(str(amount))
    tx_type=tx_type.capitalize()
    account = (
        db.query(SavingsAccount)
        .filter(SavingsAccount.account_id == account_id)
        .first()
    )

    if not account:
        raise ValueError("Account not found")

    # Update balance correctly
    if tx_type == "Deposit":
        account.balance += amount
    elif tx_type == "Withdrawal":
        if account.balance < amount:
            raise ValueError("Insufficient funds")
        account.balance -= amount
    else:
        raise ValueError("Invalid transaction type")

    # Create transaction record
    transaction = Transactions(
        account_id=account_id,
        transaction_type=tx_type,
        amount_to_be_withdrawn_or_added=amount
    )

    db.add(transaction)

    # Commit BOTH changes together
    db.commit()
    db.refresh(account)

    return account


@router.post("/{customer_id}/loan_payment")
def loan_payment(
    loan_id: uuid.UUID,
    payment_amount: float,
    payment_type: str,
    db: Session = Depends(get_db)
):

    payment_amount = Decimal(str(payment_amount))
    payment_type=payment_type.capitalize()
    loan = (
        db.query(Loan)
        .filter(Loan.loan_id == loan_id)
        .first()
    )

    if not loan:
        raise ValueError("Loan not found")

    # Update balance correctly
    if payment_type == "Standard":
        standard_loan_payment(loan, payment_amount) 

    else:
        raise ValueError("Invalid transaction type")

    # Create transaction record
    payment = LoanPayment(
        loan_id=loan_id,
        payment_amount=payment_amount,
        payment_type=payment_type,
        
    )

    db.add(payment)

    # Commit BOTH changes together
    db.commit()
    db.refresh(loan)

    return loan