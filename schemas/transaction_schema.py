from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    account_id: uuid.UUID
    transaction_type: str
    amount_to_be_withdrawn_or_added: Decimal


class TransactionUpdate(BaseModel):
    transaction_type: Optional[str] = None
    amount_to_be_withdrawn_or_added: Optional[Decimal] = None