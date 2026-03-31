from sqlalchemy.orm import Session
from models.models import EmploymentDetails
from models.models import EmploymentDetails
from schemas.customer_schema import CustomerCreate
from schemas.employment_details_schema import EmploymentCreate, EmploymentUpdate
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid

def create_employment_details(db: Session, employment_data:EmploymentCreate):
    new_member = EmploymentDetails(
        employer_first_name=employment_data.employer_first_name,
        employer_last_name=employment_data.employer_last_name,
        customer_id=employment_data.customer_id,
        job_title=employment_data.job_title,
        monthly_income=employment_data.monthly_income,
        employment_type=employment_data.employment_type,
        employment_start_date=employment_data.employment_start_date
    )
    
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def update_employment_details(db: Session, employment_id: uuid.UUID, employment_update: EmploymentUpdate):
    db_employment = db.query(EmploymentDetails).filter(EmploymentDetails.id == employment_id).first()

    if not db_employment:
        return None

    update_data = employment_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_employment, key, value)

    db.commit()
    db.refresh(db_employment)

    return db_employment

def get_member_by_id(db: Session, customer_id: uuid.UUID):
    return db.query(EmploymentDetails).filter(EmploymentDetails.id == customer_id).first()

