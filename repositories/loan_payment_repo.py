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
import logging
logger = logging.getLogger(__name__)
from log_conf import init_logging
init_logging()

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
        logger.warning(f"Loan with id {loan_payment_data.loan_id} not found for payment.")
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
    logger.info(f"Loan payment created successfully for loan_id: {loan_payment_data.loan_id} with payment_id: {payment.payment_id}")
    return new_payment

def get_loan_payment(db: Session, payment_id: uuid.UUID):
    payment = db.query(LoanPayment).filter(LoanPayment.payment_id == payment_id).first()
    if not payment:
        logger.warning(f"Loan payment with id {payment_id} not found.")
        raise HTTPException(status_code=404, detail="Loan payment not found")
    logger.info(f"Retrieved loan payment with id {payment_id} for loan_id: {payment.loan_id}")
    return payment

def get_loan_payments_by_loan(db: Session, loan_id: uuid.UUID):
    payment=db.query(LoanPayment).filter(LoanPayment.loan_id == loan_id).all()
    if not payment:
        logger.info(f"No loan payments found for loan_id: {loan_id}")
        raise ValueError(f"No loan payments found for loan_id: {loan_id}")
    logger.info(f"Fetching loan payments for loan_id: {loan_id}")
    return payment

def delete_loan_payment(db: Session, payment_id: uuid.UUID):
    payment = db.query(LoanPayment).filter(LoanPayment.payment_id == payment_id).first()
    if not payment:
        logger.info(f"Loan payment with id {payment_id} not found for deletion.")
        raise ValueError(f"Loan payment with id {payment_id} not found for deletion.")
    logger.info(f"Deleting loan payment with id {payment_id} for loan_id: {payment.loan_id}")
    db.delete(payment)
    db.commit()
    return True

def update_loan_payment(db: Session, payment_id: uuid.UUID, loan_payment_data: LoanPayments):
    payment = db.query(LoanPayment).filter(LoanPayment.payment_id == payment_id).first()
    if not payment:
        logger.info(f"Loan payment with id {payment_id} not found for update.")
        raise ValueError(f"Loan payment with id {payment_id} not found for update.")

    update_data = loan_payment_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(payment, key, value)
    logger.info(f"Updating loan payment with id {payment_id} for loan_id: {payment.loan_id} with data: {update_data}")
    db.commit()
    db.refresh(payment)
    return payment