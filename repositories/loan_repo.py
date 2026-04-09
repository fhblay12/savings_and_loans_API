from models.models import Loan, Collateral
from sqlalchemy.orm import Session
from schemas.loan_schema import LoanCreate, LoanUpdate
from schemas.collateral_schema import Collateral_schema
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException, Depends
from database import get_db
import logging
from log_conf import init_logging
init_logging()
logger = logging.getLogger(__name__)


def create_loan_details(db: Session, loan, admin, customer_id):

    new_member = Loan(
        **loan.dict(),
        customer_id=customer_id,
        admin_id=admin.admin_id,
        loan_status="Pending",
        is_verified=False,
        created_date= datetime.now()
    )
    if not new_member:
        logger.error("Failed to create loan details.")
        raise ValueError("Failed to create loan details.")
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    logger.info(f"Loan details created successfully for customer_id: {customer_id} with loan_id: {new_member.loan_id}")
    return new_member

def update_loan_details(db: Session, loan_id: uuid.UUID, loan_update: LoanUpdate):
    db_loan = db.query(Loan).filter(Loan.loan_id == loan_id).first()

    if not db_loan:
        logger.error(f"Loan with id {loan_id} not found for update.")
        raise ValueError(f"Loan with id {loan_id} not found.")

    update_data = loan_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_loan, key, value)
    logger.info(f"Loan with id {loan_id} updated successfully.")
    db.commit()
    db.refresh(db_loan)

    return db_loan  

def get_loans(db: Session, customer_id: uuid.UUID):
    return db.query(Loan).filter(Loan.customer_id == customer_id).all()

def get_loan_by_id(db: Session, loan_id: uuid.UUID):
    return db.query(Loan).filter(Loan.loan_id == loan_id).first()

def delete_loan(db: Session, loan_id: uuid.UUID):
    try:
        loan = db.query(Loan).filter(Loan.loan_id == loan_id).first()
        if not loan:
            logger.error(f"Loan with id {loan_id} not found for deletion.")
            raise ValueError(f"Loan with id {loan_id} not found.")
        db.delete(loan)
        db.commit()
        logger.info(f"Loan with id {loan_id} deleted successfully.")
        return loan
    except Exception as e:
        logger.error(f"Error occurred while deleting loan with id {loan_id}: {str(e)}")
        raise ValueError(f"Error occurred while deleting loan with id {loan_id}: {str(e)}")


def create_collateral(db: Session, collateral_data: Collateral_schema, loan_id):

    new_member = Collateral(
        loan_id=loan_id,
        collateral_type=collateral_data.collateral_type,
        collateral_value=collateral_data.collateral_value
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member