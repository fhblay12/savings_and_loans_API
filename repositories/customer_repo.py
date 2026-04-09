from sqlalchemy.orm import Session
from models.models import Customer, SavingsAccount, Transactions, Loan, LoanPayment
from schemas.customer_schema import CustomerCreate, CustomerUpdate, LoginRequest
from schemas.transaction_schema import Transaction
from schemas.loan_payment_schema import LoanPayments
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import Request
from database import SessionLocal
from fastapi import APIRouter, HTTPException, Depends
import logging
logger = logging.getLogger(__name__)
from log_conf import init_logging
init_logging()
def create_customer(db: Session, customer_data:CustomerCreate):
    hashed_pw = hash_password(customer_data.password)
    new_member = Customer(
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        address=customer_data.address,
        social_security_number=customer_data.social_security_number,
        government_ID=customer_data.government_ID,
        email=customer_data.email,
        phone_number=customer_data.phone_number,
        DOB=customer_data.DOB,
        credit_score=customer_data.credit_score,
        password=hashed_pw
    )
    if not isinstance(customer_data.password, str):
        logger.error(f"Password is not a string: {customer_data.password} (type: {type(customer_data.password)})")
        raise ValueError("Password must be a string")
    logger.info(f"Creating customer with email: {customer_data.email}, name: {customer_data.first_name} {customer_data.last_name}")
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def update_customer(db: Session, customer_id: uuid.UUID, customer_update: CustomerUpdate):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()

    if not db_customer:
        logger.warning(f"Customer with ID {customer_id} not found for update")
        raise ValueError("Customer not found")

    update_data = customer_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_customer, key, value)
    logger.info(f"Updated customer with ID {customer_id} with data: {update_data}")
    db.commit()
    db.refresh(db_customer)

    return db_customer

def customer_login(db: Session, customer_data: LoginRequest):
    # find customer by email
    customer = db.query(Customer).filter(Customer.email == customer_data.email).first()

    if not customer:
        logger.warning(f"Login failed for email {customer_data.email}: user not found")
        raise ValueError("Invalid email or password")

    # verify password
    if not verify_password(customer_data.password, customer.password):
        logger.warning(f"Login failed for email {customer_data.email}: invalid password")
        raise ValueError("Invalid email or password")

    return customer

def delete_customer(db: Session, customer_id: uuid.UUID):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()

    if not customer:
        logger.warning(f"Customer with ID {customer_id} not found for deletion")
        raise ValueError("Customer not found")

    db.delete(customer)
    db.commit()
    logger.info(f"Deleted customer with ID {customer_id}")
    return customer

def get_member_by_id(db: Session, customer_id: uuid.UUID):
    user =db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not user:
        logger.warning(f"Customer with ID {customer_id} not found")
        raise ValueError("Customer not found")
    logger.info(f"Retrieved customer with ID {customer_id}: {user.first_name} {user.last_name}")
    return user

def get_savings_accounts(db: Session, customer_id: uuid.UUID):
    # Query the account
    account = (
        db.query(SavingsAccount)
        .filter(SavingsAccount.customer_id == customer_id)
        .first()
    )

    if not account:
        logger.warning(f"Savings account for customer with ID {customer_id} not found")
        raise ValueError("Savings account not found")

    # Simply return the ORM object
    logger.info(f"Retrieved savings account for customer with ID {customer_id}: Account ID {account.account_id}, Balance {account.balance}")
    return account  # ✅ Pydantic can convert it with from_attributes=True

def get_loans(db: Session, customer_id: uuid.UUID):
    # Query the account
    loans = (
        db.query(Loan)
        .filter(Loan.customer_id == customer_id)
        .all()
    )

    if not loans:
        logger.warning(f"Loans for customer with ID {customer_id} not found")
        raise ValueError("Loans not found")
    logger.info(f"Retrieved {len(loans)} loans for customer with ID {customer_id}")
    # Simply return the ORM object
    return loans 

def transaction(db: Session, transaction_data:Transaction):
    new_member = Transactions(
        account_id=transaction_data.account_id,
        transaction_type=transaction_data.transaction_type,
        transaction_amount=transaction_data.amount_to_be_withdrawn_or_added,
    )

def loan_payment(db: Session, loan_payment_data: LoanPayments):
    new_member = LoanPayment(
        loan_id=loan_payment_data.loan_id,
        payment_amount=loan_payment_data.payment_amount,
        payment_type=loan_payment_data.payment_type
    )