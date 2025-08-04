# routers/domain_system.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.domain_system import DomainSystemCreate, DomainSystemOut
from ..crud import domain_system

router = APIRouter(prefix="/domain-system", tags=["Domain ↔ System Links"])


@router.post("/", response_model=DomainSystemOut)
def link_system_to_domain(link: DomainSystemCreate, db: Session = Depends(get_db)):
    return domain_system.create_domain_system(db, link)


@router.get("/{domain_id}", response_model=list[DomainSystemOut])
def get_systems_for_domain(domain_id: str, db: Session = Depends(get_db)):
    return domain_system.get_systems_by_domain(db, domain_id)


@router.delete("/", response_model=dict)
def unlink_system_from_domain(domain_id: str, system_id: str, db: Session = Depends(get_db)):
    return domain_system.delete_domain_system(db, domain_id, system_id)
