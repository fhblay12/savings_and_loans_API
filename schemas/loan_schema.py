from typing import Optional

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


class LoanRes(BaseModel):
    owner_id: uuid.UUID
    owner_first_name: str
    owner_last_name: str
    loan_amount: Decimal
    loan_status: str
    creation_date: datetime
    time_of_closure: Optional[datetime] = None
    is_verified: bool
    
class LoanResponse(BaseModel):
    customer_id: Optional[uuid.UUID] = None
    loan_amount: Optional[Decimal] = None
    created_date: Optional[datetime] = None
    time_of_closure: Optional[datetime] = None
    loan_type: Optional[str] = None
    loan_status: Optional[str] = None
    interest_rate: Optional[Decimal] = None

    class Config:
        from_attributes = True

class LoanUpdate(BaseModel):
    customer_id: Optional[uuid.UUID] = None
    loan_amount: Optional[Decimal] = None
    created_date: Optional[datetime] = None
    time_of_closure: Optional[datetime] = None
    loan_type: Optional[str] = None
    loan_status: Optional[str] = None
    interest_rate: Optional[Decimal] = None

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