from sqlalchemy.orm import Session
from models.models import EmploymentDetails
from models.models import EmploymentDetails
from schemas.customer_schema import CustomerCreate
from schemas.employment_details_schema import EmploymentCreate
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid

def create_employment_details(db: Session, employment_data:EmploymentCreate):
    hashed_pw = hash_password(employment_data.password)
    new_member = EmploymentDetails(
        employer_first_name=employment_data.employer_first_name,
        employer_last_name=employment_data.employer_last_name,
        customer_id=employment_data.customer_id,
        job_title=employment_data.job_title,
        employment_type=employment_data.employment_type,
        employment_start_date=employment_data.employment_start_date
    )
    
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def get_member_by_id(db: Session, customer_id: uuid.UUID):
    return db.query(EmploymentDetails).filter(EmploymentDetails.id == customer_id).first()

