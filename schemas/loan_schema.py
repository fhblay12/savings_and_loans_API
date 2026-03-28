from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone, datetime
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID
from fastapi import Depends, Form


class LoanCreate(BaseModel):
    loan_amount: int
    loan_type: str
    term_in_months: int


class LoanResponse(BaseModel):
    customer_id: uuid.UUID
    loan_amount: Decimal
    created_date: datetime
    time_of_closure: datetime
    loan_type: str
    loan_status: str
    interest_rate: Decimal

    class Config:
        from_attributes = True

def loan_form(
    loan_amount: int = Form(...),
    loan_type: str = Form(...),
    term_in_months: int = Form(...)
) -> LoanCreate:
    return LoanCreate(
        loan_amount=loan_amount,
        loan_type=loan_type,
        term_in_months=term_in_months,
    )