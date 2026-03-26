from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone, datetime
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID

class Collateral_schema(BaseModel):
    collateral_type: str
    collateral_value: str