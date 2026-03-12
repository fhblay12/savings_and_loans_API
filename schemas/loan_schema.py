from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone, datetime
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID

class LoanCreate(BaseModel):
    customer_id: uuid.UUID
    admin_id: uuid.UUID
    loan_amount: int
    loan_type: str
    loan_status: str
    loan_term: int
    loan_type: str
    is_verified: bool
    created_date: datetime
  