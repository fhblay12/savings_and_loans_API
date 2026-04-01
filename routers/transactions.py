


from decimal import Decimal
import uuid
from services.transaction_service import make_transaction
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.models import SavingsAccount, Transactions

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/{customer_id}/transaction")
def create_transaction(
    account_id: uuid.UUID,
    amount: float,
    tx_type: str,
    db: Session = Depends(get_db)
):
    account=create_transaction(account_id, amount, tx_type, db)
    return account


@router.get("/{account_id}/transactions")
def get_transactions(transaction_id: uuid.UUID, db: Session = Depends(get_db)): 
    transactions = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).all()
    return { "transactions": transactions }

@router.delete("/transaction/{transaction_id}")
def delete_transaction(transaction_id: uuid.UUID, db: Session = Depends(get_db)):
    transaction = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).first()
    if not transaction:
        raise ValueError("Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}  

@router.patch("/transaction/{transaction_id}")
def update_transaction(transaction_id: uuid.UUID, amount: float, tx_type: str, db: Session = Depends(get_db)):
    transaction = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).first()
    if not transaction:
        raise ValueError("Transaction not found")
    
    # Update transaction details
    amount=transaction.amount_to_be_withdrawn_or_added = Decimal(str(amount))
    tx_type=transaction.transaction_type = tx_type.capitalize()
    make_transaction(db=db, account_id=transaction.account_id, amount=amount, tx_type=tx_type)
    
    db.commit()
    db.refresh(transaction)
    return transaction