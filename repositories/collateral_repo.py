from models.models import Loan, Collateral
from sqlalchemy.orm import Session
from schemas.collateral_schema import Collateral_schema
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dateutil.relativedelta import relativedelta

def create_collateral_details(db: Session, collateral_data, loan_id ):

    new_member = Collateral(
        loan_id=loan_id,
        collateral_type=collateral_data.collateral_type,
        collateral_value=collateral_data.collateral_value
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member