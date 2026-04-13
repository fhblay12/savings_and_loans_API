
import uuid

from fastapi import Depends, Request
from plotly.io import templates
from requests import Session
from starlette.responses import HTMLResponse
from database import get_db
from models.models import Collateral
from repositories.collateral_repo import create_collateral_details, get_collateral_by_id, delete_collateral, update_collateral
from schemas.collateral_schema import Collateral_schema, collateral_form
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
    try:
        new_collateral = create_collateral_details(db, collateral, loan_id)
        return  { "collateral": new_collateral } 
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{collateral_id}")
def collateral(request: Request, collateral_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        collateral = get_collateral_by_id(db, collateral_id)
        return collateral
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{collateral_id}")
def delete_collaterals(collateral_id: uuid.UUID, db: Session = Depends(get_db)): 
    try:
        collateral = delete_collateral(db, collateral_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Collateral deleted successfully"}

@router.patch("/update/{collateral_id}")
def update_collaterals(collateral_id: uuid.UUID, collateral_update: Collateral_schema, db: Session = Depends(get_db)):
    try:
        collateral = update_collateral(db, collateral_id, collateral_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))