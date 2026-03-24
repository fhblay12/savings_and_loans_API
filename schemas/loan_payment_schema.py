from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone, datetime
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID

class LoanPayments(BaseModel):
    loan_id: uuid.UUID
    payment_amount: Decimal
    payment_type: str

