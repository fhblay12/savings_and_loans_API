

from typing import Literal

from core.security import get_current_user
from schemas.transaction_schema import Transaction, TransactionUpdate
from repositories.transaction_repo import create_transaction, get_transaction, delete_transaction, update_transaction
from decimal import Decimal
import uuid
from services.transaction_service import make_transaction
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import SavingsAccount, Transactions

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/{customer_id}/transaction")
def create_transactions(
    account_id: uuid.UUID,
    amount: Decimal,
    tx_type: Literal["Deposit", "Withdrawal"],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return make_transaction(db, account_id, amount, tx_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{account_id}/transactions")
def get_transactions(transaction_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)): 
    try:
        transactions = get_transaction(db, transaction_id)
        return { "transactions": transactions }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.delete("/transaction/{transaction_id}")
def delete_transaction(transaction_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        delete_transaction(db, transaction_id)
        return {"message": "Transaction deleted successfully"} 
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
     

@router.patch("/transaction/{transaction_id}")
def update_transactions(transaction_update: TransactionUpdate, transaction_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        transaction = update_transaction(db, transaction_id, transaction_update.amount_to_be_withdrawn_or_added, transaction_update.transaction_type)
        return {"message": "Transaction updated successfully", "transaction": transaction}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))