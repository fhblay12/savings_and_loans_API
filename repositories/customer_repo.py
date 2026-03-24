from sqlalchemy.orm import Session
from models.models import Customer, SavingsAccount, Transactions, Loan, LoanPayment
from schemas.customer_schema import CustomerCreate, LoginRequest
from schemas.transaction_schema import Transaction
from schemas.loan_payment_schema import LoanPayments
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid

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
    print(f"Password type: {type(customer_data.password)}, length: {len(customer_data.password)}")
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member
def customer_login(db: Session, customer_data: LoginRequest):
    # find customer by email
    customer = db.query(Customer).filter(Customer.email == customer_data.email).first()

    if not customer:
        return None

    # verify password
    if not verify_password(customer_data.password, customer.password):
        return None

    return customer


def get_member_by_id(db: Session, customer_id: uuid.UUID):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_savings_accounts(db: Session, customer_id: uuid.UUID):
    # Query the account
    account = (
        db.query(SavingsAccount)
        .filter(SavingsAccount.customer_id == customer_id)
        .first()
    )

    if not account:
        return None  # or raise HTTPException(status_code=404)

    # Simply return the ORM object
    return account  # ✅ Pydantic can convert it with from_attributes=True

def get_loans(db: Session, customer_id: uuid.UUID):
    # Query the account
    loans = (
        db.query(Loan)
        .filter(Loan.customer_id == customer_id)
        .all()
    )

    if not loans:
        return None  # or raise HTTPException(status_code=404)

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