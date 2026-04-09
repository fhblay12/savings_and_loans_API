from sqlalchemy.orm import Session
from models.models import Customer, SavingsAccount, Transactions, Loan, LoanPayment
from schemas.loan_payment_schema import LoanPayments
from datetime import datetime
from schemas.transaction_schema import Transaction
from schemas.loan_payment_schema import LoanPayments
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal
from database import get_db
from models.models import Loan, LoanPayment
from services.customer_loan_payment_services import standard_loan_payment
def create_loan_payment(db: Session, loan_payment_data: LoanPayments):
    new_payment = LoanPayment(
        loan_id=loan_payment_data.loan_id,
        payment_amount=loan_payment_data.payment_amount,
        payment_date=datetime.utcnow()
    )
    payment_amount = Decimal(str(loan_payment_data.payment_amount)) 
    payment_type=loan_payment_data.payment_type.capitalize()
    loan = (
        db.query(Loan)
        .filter(Loan.loan_id == loan_payment_data.loan_id)
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
        loan_id=loan_payment_data.loan_id,
        payment_amount=payment_amount,
        payment_type=payment_type,
        
    )

    db.add(payment)

    # Commit BOTH changes together
    db.commit()
    db.refresh(loan)
    db.refresh(payment)
    return new_payment

def get_loan_payment(db: Session, payment_id: uuid.UUID):
    return db.query(LoanPayment).filter(LoanPayment.payment_id == payment_id).first()

def get_loan_payments_by_loan(db: Session, loan_id: uuid.UUID):
    return db.query(LoanPayment).filter(LoanPayment.loan_id == loan_id).all()   

def delete_loan_payment(db: Session, payment_id: uuid.UUID):
    payment = db.query(LoanPayment).filter(LoanPayment.payment_id == payment_id).first()
    if payment:
        db.delete(payment)
        db.commit()
        return True
    return False

def update_loan_payment(db: Session, payment_id: uuid.UUID, loan_payment_data: LoanPayments):
    payment = db.query(LoanPayment).filter(LoanPayment.payment_id == payment_id).first()
    if not payment:
        return None

    update_data = loan_payment_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment