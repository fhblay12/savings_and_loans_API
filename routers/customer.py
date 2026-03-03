from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.customer_schema import CustomerCreate
from repositories.customer_repo import create_customer
from core.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM
from models.models import Customer
from schemas.customer_schema import LoginRequest
from database import get_db
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt

router = APIRouter(prefix="/customer", tags=["Customer"])





@router.post("/")
def create_registration_endpoint(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(Customer).filter(Customer.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    token = create_access_token({"sub": user.email, "id": str(user.customer_id)})
    return {"access_token": token, "token_type": "bearer"}



class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.post("/refresh", response_model=Token)
def refresh_token_endpoint(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Issue new access token (optional: new refresh token)
        access_token = create_access_token({"sub": user_id})
        return {"access_token": access_token, "refresh_token": refresh_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")