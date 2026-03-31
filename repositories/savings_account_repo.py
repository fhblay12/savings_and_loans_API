from sqlalchemy.orm import Session
from models.models import SavingsAccount
from schemas.savings_account_schema import SavingsAccountCreate, SavingsAccountUpdate
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid

def create_savings_account_repo(db: Session, account_data:SavingsAccountCreate):
    new_member = SavingsAccount(
        customer_id=account_data.customer_id,
        balance=account_data.balance,
        admin_id=account_data.admin_id,
        is_verified=account_data.is_verified

    )
    
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


def update_savings_account(db: Session, account_id: uuid.UUID, account_update: SavingsAccountUpdate):
    db_account = db.query(SavingsAccount).filter(SavingsAccount.account_id == account_id).first()

    if not db_account:
        return None

    update_data = account_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_account, key, value)

    db.commit()
    db.refresh(db_account)

    return db_account


