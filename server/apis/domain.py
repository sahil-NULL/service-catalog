from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from ..crud import domain as crud
from ..schemas.domain import DomainOut, DomainCreate, DomainUpdate

router = APIRouter(prefix="/domains", tags=["Domains"])

@router.get("/", response_model=list[DomainOut])
def read_domains(db: Session = Depends(get_db)):
    return crud.get_all_domains(db)

@router.post("/", response_model=DomainOut)
def create_domain(domain: DomainCreate, db: Session = Depends(get_db)):
    return crud.create_domain(db, domain)


@router.get("/{domain_id}", response_model=DomainOut)
def read_domain(domain_id: str, db: Session = Depends(get_db)):
    db_domain = crud.get_domain(db, domain_id)
    if not db_domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return db_domain


@router.get("/organisation/{org_id}", response_model=list[DomainOut])
def read_domains_for_org(org_id: str, db: Session = Depends(get_db)):
    return crud.get_domains_by_organisation(db, org_id)


@router.put("/{domain_id}", response_model=DomainOut)
def update_domain(domain_id: str, domain: DomainUpdate, db: Session = Depends(get_db)):
    updated = crud.update_domain(db, domain_id, domain)
    if not updated:
        raise HTTPException(status_code=404, detail="Domain not found")
    return updated


@router.delete("/{domain_id}", response_model=DomainOut)
def delete_domain(domain_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_domain(db, domain_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Domain not found")
    return deleted
