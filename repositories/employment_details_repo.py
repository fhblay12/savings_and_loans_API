from sqlalchemy.orm import Session
from models.models import EmploymentDetails
from models.models import EmploymentDetails
from schemas.customer_schema import CustomerCreate
from schemas.employment_details_schema import EmploymentCreate, EmploymentUpdate
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from fastapi import APIRouter, Depends, HTTPException, logger, status

logger = logger.getLogger(__name__)
from log_conf import init_logging
init_logging()
def create_employment_details(db: Session, employment_data:EmploymentCreate):
    try:
        new_member = EmploymentDetails(
            employer_first_name=employment_data.employer_first_name,
            employer_last_name=employment_data.employer_last_name,
            customer_id=employment_data.customer_id,
            job_title=employment_data.job_title,
            monthly_income=employment_data.monthly_income,
            employment_type=employment_data.employment_type,
            employment_start_date=employment_data.employment_start_date
        )
    except Exception as e:
        logger.error(f"Error occurred while creating employment details: {e}")
        raise ValueError("Failed to create employment details")   
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def update_employment_details(db: Session, employment_id: uuid.UUID, employment_update: EmploymentUpdate):
    try:
        employment = db.query(EmploymentDetails).filter(EmploymentDetails.id == employment_id).first()
    except Exception as e:
        logger.error(f"Error occurred while fetching employment details: {e}")
        raise ValueError("Failed to fetch employment details")

    if not employment:
        raise ValueError
    employment.employer_first_name = employment_update.employer_first_name
    employment.employer_last_name = employment_update.employer_last_name
    employment.job_title = employment_update.job_title
    employment.monthly_income = employment_update.monthly_income
    employment.employment_type = employment_update.employment_type
    db.commit()
    db.refresh(employment)
    logger.info(f"Updated employment details with ID {employment_id}")
    return employment

def delete_employment_details(db: Session, employment_id: uuid.UUID):
    try:
        employment = db.query(EmploymentDetails).filter(EmploymentDetails.employment_details_id == employment_id).first()
    except Exception as e:
        logger.error(f"Error occurred while fetching employment details: {e}")
        raise ValueError("Failed to fetch employment details")

    if not employment:
        raise ValueError("Employment details not found")
    db.delete(employment)
    db.commit()
    return employment

def get_member_by_id(db: Session, customer_id: uuid.UUID):
    try:
        employment = db.query(EmploymentDetails).filter(EmploymentDetails.id == customer_id).first()
    except Exception as e:
        logger.error(f"Error occurred while fetching employment details: {e}")
        raise ValueError("Failed to fetch employment details")

    if not employment:
        raise ValueError("Employment details not found")
    return employment

