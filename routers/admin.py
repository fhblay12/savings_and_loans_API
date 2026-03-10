from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
from typing import List
from database import get_db
from models.models import Admin, SavingsAccount, Customer
from schemas.admin_schema import AdminCreate, SavingAccountAdmin
from repositories.admin_repo import create_admin, get_admin_savings_accounts
from core.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM
import uuid

router = APIRouter(prefix="/admin", tags=["Admin"])


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register")
def create_admin_user(admin: AdminCreate, db: Session = Depends(get_db)):
    return create_admin(db, admin)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(Admin).filter(Admin.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": str(user.admin_id), "email": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
def refresh_token_endpoint(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        access_token = create_access_token({"sub": user_id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.get("/{admin_id}/savings-accounts", response_model=List[SavingAccountAdmin])
def get_savings_accounts_for_admin(
    admin_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    accounts = get_admin_savings_accounts(db, admin_id)

    if not accounts:
        raise HTTPException(status_code=404, detail="No savings accounts found for this admin")

    return accounts