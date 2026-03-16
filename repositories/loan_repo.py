from models.models import Loan
from sqlalchemy.orm import Session
from schemas.loan_schema import LoanCreate
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
        time_of_closure=toc,
        created_date=loan_data.created_date
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member