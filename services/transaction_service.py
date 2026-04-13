
from decimal import Decimal

import uuid

from models.models import SavingsAccount, Transactions

from sqlalchemy.orm import Session
from repositories.transaction_repo import create_transaction, get_transaction, delete_transaction, update_transaction
from sqlalchemy.orm import Session


def make_transaction (db: Session, account_id: uuid.UUID, amount: Decimal, tx_type: str):
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