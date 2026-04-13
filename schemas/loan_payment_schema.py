from typing import Optional

from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone, datetime
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID

class LoanPayments(BaseModel):
    payment_amount: float
    payment_type: Optional[str] = None