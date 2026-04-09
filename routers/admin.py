from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
from typing import List
from database import get_db
from models.models import Admin, SavingsAccount, Customer, Loan
from schemas.admin_schema import AdminCreate, AdminUpdate, LoginRequest, SavingAccountAdmin, LoanAdmin
from schemas.loan_schema import LoanRes
from repositories.admin_repo import create_admin, login_admin, update_admin, delete_admin, get_admin_savings_accounts, get_admin_loans, get_admin_unverified_savings_accounts, verify_accounts, get_admin_unverified_loans
from core.security import create_access_token, SECRET_KEY, ALGORITHM, get_current_user, get_current_admin
from core.password import hash_password, verify_password
import uuid
from core.dependencies import require_roles
from schemas.loan_schema import LoanResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register")
def create_admin_user(admin: AdminCreate, db: Session = Depends(get_db)):
    try:
        new_admin = create_admin(db, admin)
        return new_admin
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        admin=login_admin(db, LoginRequest(email=form_data.username, password=form_data.password))
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    access_token = create_access_token(
        {"sub": str(admin.admin_id), "email": admin.email, "type": "admin",
            "role": admin.admin_role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.patch("/update/{admin_id}")
def update_admins(admin_id: uuid.UUID, admin_update: AdminUpdate, db: Session = Depends(get_db)):
    try:
        updated_admin = update_admin(db=db, admin_id=admin_id, admin_update=admin_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return updated_admin
      
@router.delete("/delete/{admin_id}")
def delete_admin(admin_id: uuid.UUID, db: Session = Depends(get_db)):    
    try:
        admin = delete_admin(db=db, admin_id=admin_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"detail": "Admin deleted successfully"}

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
    db: Session = Depends(get_db),
    admin = Depends(require_roles(["Account Administrator"]))
):
    try:
        accounts = get_admin_savings_accounts(db, admin_id)
        return accounts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class VerifyAccountsRequest(BaseModel):
    account_ids: List[uuid.UUID]

@router.get("/admin/{admin_id}/unverified-accounts")
def get_unverified_accounts(admin_id: uuid.UUID, db: Session = Depends(get_db), admin = Depends(require_roles(["Account Administrator"])) ):
    try:
        accounts = get_admin_unverified_savings_accounts(db, admin_id)
        return accounts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{admin_id}/verify-accounts")
def verify_accounts(request: VerifyAccountsRequest, db: Session = Depends(get_db), admin = Depends(require_roles(["Account Administrator"]))):
    try:
        verify_accounts(db, request.account_ids)
        return {"detail": f"{len(request.account_ids)} account(s) verified successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class VerifyLoansRequest(BaseModel):
    loan_ids: List[uuid.UUID]

@router.get("/{admin_id}/unverified-loans", response_model=List[LoanResponse])
def get_unverified_accounts(db: Session = Depends(get_db),
                            admin = Depends(require_roles(["Loan Officer"]))):
    try:
        loans = get_admin_unverified_loans(db, admin.admin_id)
        return loans
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{admin_id}/verify-loans")
def verify_accounts(request: VerifyLoansRequest, db: Session = Depends(get_db), admin = Depends(require_roles(["Loan Officer"]))):
    try:
        verify_accounts(db, request.loan_ids)
        return {"detail": f"{len(request.loan_ids)} loan(s) verified successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{admin_id}/loans", response_model=List[LoanRes])
def get_loans_for_admin(
    admin_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin = Depends(require_roles(["Loan Officer"]))
):
    try:
        loans = get_admin_loans(db, admin_id)
        return loans
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
  