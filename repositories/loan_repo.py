from models.models import Loan, Collateral
from sqlalchemy.orm import Session
from schemas.loan_schema import LoanCreate, LoanUpdate
from schemas.collateral_schema import Collateral_schema
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dateutil.relativedelta import relativedelta

def create_loan_details(db: Session, loan, admin, customer_id):

    new_member = Loan(
        **loan.dict(),
        customer_id=customer_id,
        admin_id=admin.admin_id,
        loan_status="Pending",
        is_verified=False,
        created_date= datetime.now()
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member

def update_loan_details(db: Session, loan_id: uuid.UUID, loan_update: LoanUpdate):
    db_loan = db.query(Loan).filter(Loan.loan_id == loan_id).first()

    if not db_loan:
        return None

    update_data = loan_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_loan, key, value)

    db.commit()
    db.refresh(db_loan)

    return db_loan  

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