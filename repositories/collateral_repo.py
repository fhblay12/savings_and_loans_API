from models.models import Loan, Collateral
from sqlalchemy.orm import Session
from schemas.collateral_schema import Collateral_schema
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException, Depends, logger
logger = logger.getLogger(__name__)
from log_conf import init_logging
init_logging()

def create_collateral_details(db: Session, collateral_data, loan_id ):
    existing_collateral = db.query(Collateral).filter(Collateral.loan_id == loan_id).first()
    if existing_collateral:
        logger.warning(f"Collateral for loan ID {loan_id} already exists with collateral ID {existing_collateral.collateral_id}")
        raise ValueError("Collateral for this loan already exists")
    new_member = Collateral(
        loan_id=loan_id,
        collateral_type=collateral_data.collateral_type,
        collateral_value=collateral_data.collateral_value
    )
    logger.info(f"Creating collateral for loan ID {loan_id} with type {collateral_data.collateral_type} and value {collateral_data.collateral_value}")
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member

def get_collateral_by_id(db: Session, collateral_id: uuid.UUID):
    collateral = db.query(Collateral).filter(Collateral.collateral_id == collateral_id).first()
    if not collateral:
        logger.warning(f"Collateral with ID {collateral_id} not found")
        raise HTTPException(status_code=404, detail="Collateral not found")
    logger.info(f"Retrieved collateral with ID {collateral_id} for loan ID {collateral.loan_id}")
    return collateral

def delete_collateral(db: Session, collateral_id: uuid.UUID):
    collateral = db.query(Collateral).filter(Collateral.collateral_id == collateral_id).first()
    if not collateral:
        logger.warning(f"Collateral with ID {collateral_id} not found")
        raise HTTPException(status_code=404, detail="Collateral not found")
    logger.info(f"Deleting collateral with ID {collateral_id} for loan ID {collateral.loan_id}")

    db.delete(collateral)
    db.commit()
    return {"message": "Collateral deleted successfully"}

def update_collateral(db: Session, collateral_id: uuid.UUID, collateral_update: Collateral_schema):
    collateral = db.query(Collateral).filter(Collateral.collateral_id == collateral_id).first()
    if not collateral:
        logger.warning(f"Collateral with ID {collateral_id} not found")
        raise HTTPException(status_code=404, detail="Collateral not found")
    logger.info(f"Updating collateral with ID {collateral_id} for loan ID {collateral.loan_id}")

    collateral.collateral_type = collateral_update.collateral_type
    collateral.collateral_value = collateral_update.collateral_value
    db.commit()
    db.refresh(collateral)
    return collateral