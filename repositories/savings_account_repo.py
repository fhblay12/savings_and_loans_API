from sqlalchemy.orm import Session
from models.models import SavingsAccount
from schemas.savings_account_schema import SavingsAccountCreate
from datetime import datetime
from core.security import hash_password
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


