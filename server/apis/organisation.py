from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..crud import organisation as crud
from ..schemas.organisation import OrganisationCreate, OrganisationUpdate, OrganisationOut

router = APIRouter(prefix="/organisations", tags=["Organisations"])

@router.post("/", response_model=OrganisationOut)
def create(org: OrganisationCreate, db: Session = Depends(get_db)):
    return crud.create_organisation(db, org)

@router.get("/{org_id}", response_model=OrganisationOut)
def get(org_id: str, db: Session = Depends(get_db)):
    org = crud.get_organisation(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return org

@router.get("/", response_model=List[OrganisationOut])
def list_all(db: Session = Depends(get_db)):
    return crud.get_all_organisations(db)

@router.put("/{org_id}", response_model=OrganisationOut)
def update(org_id: str, updates: OrganisationUpdate, db: Session = Depends(get_db)):
    org = crud.update_organisation(db, org_id, updates)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return org

@router.delete("/{org_id}", response_model=OrganisationOut)
def delete(org_id: str, db: Session = Depends(get_db)):
    org = crud.delete_organisation(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return org
