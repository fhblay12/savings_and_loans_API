


from decimal import Decimal
import uuid

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

    amount = Decimal(str(amount))
    tx_type=tx_type.capitalize()
    account = (
        db.query(SavingsAccount)
        .filter(SavingsAccount.account_id == account_id)
        .first()
    )

    if not account:
        raise ValueError("Account not found")

    # Update balance correctly
    if tx_type == "Deposit":
        account.balance += amount
    elif tx_type == "Withdrawal":
        if account.balance < amount:
            raise ValueError("Insufficient funds")
        account.balance -= amount
    else:
        raise ValueError("Invalid transaction type")

    # Create transaction record
    transaction = Transactions(
        account_id=account_id,
        transaction_type=tx_type,
        amount_to_be_withdrawn_or_added=amount
    )

    db.add(transaction)

    # Commit BOTH changes together
    db.commit()
    db.refresh(account)

    return account


@router.get("/{account_id}/transactions")
def get_transactions(account_id: uuid.UUID, db: Session = Depends(get_db)): 
    transactions = db.query(Transactions).filter(Transactions.account_id == account_id).all()
    return transactions

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
    transaction.amount_to_be_withdrawn_or_added = Decimal(str(amount))
    transaction.transaction_type = tx_type.capitalize()
    
    db.commit()
    db.refresh(transaction)
    return transaction