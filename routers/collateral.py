
import uuid

from fastapi import Depends, Request
from plotly.io import templates
from requests import Session
from starlette.responses import HTMLResponse
from database import get_db
from models.models import Collateral
from repositories.collateral_repo import create_collateral_details
from core.security import create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from fastapi import APIRouter, HTTPException, Depends
from schemas.collateral_schema import Collateral_schema, collateral_form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/collateral", tags=["collateral"])

@router.post("/apply/{loan_id}/collateral")
def create_registration_endpoint(
    request: Request,
    loan_id: uuid.UUID,
    collateral: Collateral_schema = Depends(collateral_form),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
    ):
    new_collateral = create_collateral_details(db, collateral, loan_id)
    return  { "collateral": new_collateral } 

@router.get("/collateral/{collateral_id}")
def collateral(request: Request, collateral_id: uuid.UUID, db: Session = Depends(get_db)):
    collateral = db.query(Collateral).filter(Collateral.collateral_id == collateral_id).first()
    if not collateral:
        raise HTTPException(status_code=404, detail="Collateral not found")
    return collateral


@router.delete("/collateral/{collateral_id}")
def delete_collateral(collateral_id: uuid.UUID, db: Session = Depends(get_db)): 
    collateral = db.query(Collateral).filter(Collateral.collateral_id == collateral_id).first()
    if not collateral:
        raise HTTPException(status_code=404, detail="Collateral not found")
    db.delete(collateral)
    db.commit()
    return {"message": "Collateral deleted successfully"}

@router.patch("/collateral/{collateral_id}")
def update_collateral(collateral_id: uuid.UUID, collateral_update: Collateral_schema, db: Session = Depends(get_db)):
    collateral = db.query(Collateral).filter(Collateral.collateral_id == collateral_id).first()
    if not collateral:
        raise HTTPException(status_code=404, detail="Collateral not found")
    collateral.collateral_type = collateral_update.collateral_type
    collateral.collateral_value = collateral_update.collateral_value
    db.commit()
    db.refresh(collateral)
    return collateral