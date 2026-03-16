from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
from typing import List
from database import get_db
from models.models import Admin, SavingsAccount, Customer, Loan
from schemas.admin_schema import AdminCreate, SavingAccountAdmin, LoanAdmin
from repositories.admin_repo import create_admin, get_admin_savings_accounts, get_admin_loans, get_admin_unverified_savings_accounts
from core.security import create_access_token, SECRET_KEY, ALGORITHM, get_current_user, get_current_admin
from core.password import hash_password, verify_password
import uuid
from core.dependencies import require_roles

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

    admin = db.query(Admin).filter(Admin.email == form_data.username).first()
    

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": str(admin.admin_id), "email": admin.email, "type": "admin",
            "role": admin.admin_role}
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
    db: Session = Depends(get_db),
    admin = Depends(require_roles(["Account Administrator"]))
):
    accounts = get_admin_savings_accounts(db, admin_id)

    if not accounts:
        raise HTTPException(status_code=404, detail="No savings accounts found for this admin")

    return accounts


class VerifyAccountsRequest(BaseModel):
    account_ids: List[uuid.UUID]

@router.get("/admin/{admin_id}/unverified-accounts")
def get_unverified_accounts(admin_id: uuid.UUID, db: Session = Depends(get_db), admin = Depends(require_roles(["Account Administrator"])) ):
    
    accounts = get_admin_unverified_savings_accounts(db, admin_id)

    return accounts

@router.put("/{admin_id}/verify-accounts")
def verify_accounts(request: VerifyAccountsRequest, db: Session = Depends(get_db), admin = Depends(require_roles(["Account Administrator"]))):
    accounts = db.query(SavingsAccount).filter(SavingsAccount.account_id.in_(request.account_ids)).all()

    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found")

    for account in accounts:
        account.is_verified = True

    db.commit()
    return {"detail": f"{len(accounts)} account(s) verified successfully."}



class VerifyLoansRequest(BaseModel):
    loan_ids: List[uuid.UUID]

@router.get("/{admin_id}/unverified-loans", response_model=List[LoanAdmin])
def get_unverified_accounts(db: Session = Depends(get_db),
                            admin = Depends(require_roles(["Loan Officer"]))):
    loans = db.query(Loan).filter(Loan.is_verified == False).all()
    return loans

@router.put("/{admin_id}/verify-loans")
def verify_accounts(request: VerifyLoansRequest, db: Session = Depends(get_db), admin = Depends(require_roles(["Loan Officer"]))):
    accounts = db.query(Loan).filter(Loan.loan_id.in_(request.loan_ids)).all()

    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found")

    for account in accounts:
        account.is_verified = True

    db.commit()
    return {"detail": f"{len(accounts)} account(s) verified successfully."}


@router.get("/{admin_id}/loans", response_model=List[LoanAdmin])
def get_loans_for_admin(
    admin_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin = Depends(require_roles(["Loan Officer"]))
):
    loans = get_admin_loans(db, admin_id)

    if not loans:
        raise HTTPException(status_code=404, detail="No loans found for this admin")

    return loans


