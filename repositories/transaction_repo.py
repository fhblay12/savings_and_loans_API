from sqlalchemy.orm import Session
from models.models import Transactions, SavingsAccount
from schemas.transaction_schema import Transaction, TransactionUpdate
from schemas.savings_account_schema import SavingsAccountCreate, SavingsAccountUpdate
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from decimal import Decimal
from fastapi import APIRouter, HTTPException, Depends
import logging
logger = logging.getLogger(__name__)
from log_conf import init_logging


def create_transaction(account_id: uuid.UUID, amount: float, tx_type: str, db: Session):
    existing_account = db.query(SavingsAccount).filter(SavingsAccount.account_id == account_id).first()
    if not existing_account:
        logger.warning(f"Savings account with id {account_id} not found for transaction.")
        raise ValueError(f"Savings account with id {account_id} not found.")
    
    new_transaction = Transactions(
        account_id=account_id,
        amount_to_be_withdrawn_or_added=amount,
        transaction_type=tx_type.capitalize(),
        transaction_date=datetime.utcnow()
    )
    if not new_transaction:
        logger.error(f"Failed to create transaction for account_id: {account_id}.")
        raise ValueError(f"Failed to create transaction for account_id: {account_id}.")
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    logger.info(f"Transaction created successfully for account_id: {account_id} with transaction_id: {new_transaction.transaction_id}") 
    return new_transaction

def get_transactions(db: Session, transaction_id: uuid.UUID):
    transaction = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).all()
    if not transaction:
        logger.info(f"No transactions found for transaction_id: {transaction_id}")
        raise ValueError(f"No transactions found for transaction_id: {transaction_id}")
    logger.info(f"Retrieved {len(transaction)} transactions for transaction_id: {transaction_id}")
    return transaction

def delete_transaction(db: Session, transaction_id: uuid.UUID):
    transaction = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).first()
    if not transaction:
        logger.warning(f"Transaction with id {transaction_id} not found for deletion.")
        raise ValueError(f"Transaction with id {transaction_id} not found.")

    db.delete(transaction)
    db.commit()
    logger.info(f"Transaction with id {transaction_id} deleted successfully.")
    return transaction

def update_transaction(db: Session, transaction_id: uuid.UUID, amount: float, tx_type: str):
    transaction = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).first()
    if not transaction:
        logger.warning(f"Transaction with id {transaction_id} not found for update.")
        raise ValueError(f"Transaction with id {transaction_id} not found.")
    
    # Update transaction details
    transaction.amount_to_be_withdrawn_or_added = Decimal(str(amount))
    transaction.transaction_type = tx_type.capitalize()
    
    db.commit()
    db.refresh(transaction)
    logger.info(f"Transaction with id {transaction_id} updated successfully.")
    return transaction


