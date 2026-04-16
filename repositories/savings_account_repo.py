from sqlalchemy.orm import Session
from models.models import SavingsAccount
from schemas.savings_account_schema import SavingsAccountCreate, SavingsAccountUpdate
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from fastapi import HTTPException, status
import logging
logger = logging.getLogger(__name__)
from log_conf import init_logging
init_logging()
def create_savings_account_repo(db: Session, account_data:SavingsAccountCreate):
    try:
        new_member = SavingsAccount(
            customer_id=account_data.customer_id,
            balance=account_data.balance,
            admin_id=account_data.admin_id,
            is_verified=account_data.is_verified

        )
    except Exception as e:
        try:
            customer_id = account_data.customer_id
        except AttributeError:
            logger.error(f"Missing customer_id: {str(e)}")
            raise ValueError(f"Error creating savings account for customer: {str(e)}")
        logger.error(f"Error creating savings account for customer: {str(e)}")
        raise ValueError(f"Error creating savings account for customer: {str(e)}")   
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    logger.info(f"Savings account created successfully for customer_id: {account_data.customer_id} with account_id: {new_member.account_id}")
    return new_member

def get_savings_accounts(db: Session, customer_id: uuid.UUID):
    account=db.query(SavingsAccount).filter(SavingsAccount.customer_id == customer_id).all()
    if not account:
        logger.info(f"No savings accounts found for customer_id: {customer_id}")
        raise ValueError(f"No savings accounts found for customer_id: {customer_id}")
    logger.info(f"Retrieved {len(account)} savings accounts for customer_id: {customer_id}")
    return account

def delete_savings_account(db: Session, account_id: uuid.UUID):
    account = db.query(SavingsAccount).filter(SavingsAccount.account_id == account_id).first()
    if not account:
        logger.warning(f"Savings account with id {account_id} not found for deletion.")
        raise ValueError(f"Savings account with id {account_id} not found.")
    db.delete(account)
    db.commit()
    logger.info(f"Savings account with id {account_id} deleted successfully.")
    return account

def get_savings_account_by_id(db: Session, account_id: uuid.UUID):
    account=db.query(SavingsAccount).filter(SavingsAccount.account_id == account_id).first()
    if not account:
        logger.warning(f"Savings account with id {account_id} not found.")
        raise ValueError(f"Savings account with id {account_id} not found.")
    logger.info(f"Savings account with id {account_id} retrieved successfully.")
    return account

def update_savings_account(db: Session, account_id: uuid.UUID, account_update: SavingsAccountUpdate):
    db_account = db.query(SavingsAccount).filter(SavingsAccount.account_id == account_id).first()

    if not db_account:
        logger.warning(f"Savings account with id {account_id} not found for update.")
        raise ValueError(f"Savings account with id {account_id} not found.")

    update_data = account_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_account, key, value)

    db.commit()
    db.refresh(db_account)
    logger.info(f"Savings account with id {account_id} updated successfully.")
    return db_account


