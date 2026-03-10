from sqlalchemy.orm import Session
from models.models import Customer
from schemas.customer_schema import CustomerCreate, LoginRequest
from datetime import datetime
from core.security import hash_password, verify_password
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

