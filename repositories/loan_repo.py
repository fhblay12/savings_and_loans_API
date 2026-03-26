from models.models import Loan, Collateral
from sqlalchemy.orm import Session
from schemas.loan_schema import LoanCreate
from schemas.collateral_schema import Collateral_schema
from datetime import datetime
from core.password import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dateutil.relativedelta import relativedelta

def create_loan_details(db: Session, loan_data: LoanCreate):

    # calculate time of closure
    toc = loan_data.created_date + relativedelta(months=loan_data.loan_term)

    new_member = Loan(
        customer_id=loan_data.customer_id,
        admin_id=loan_data.admin_id,
        loan_amount=loan_data.loan_amount,
        term_in_months=loan_data.loan_term,
        loan_type=loan_data.loan_type,
        loan_status=loan_data.loan_status,
        is_verified=loan_data.is_verified,
        interest_rat=loan_data.interest_rate,
        time_of_closure=toc,
        created_date=loan_data.created_date
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


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