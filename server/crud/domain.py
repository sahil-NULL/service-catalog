from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from ..models.domain import Domain
from ..schemas.domain import *


# Create new domain
def create_domain(db: Session, domain: DomainCreate):
    try:
        db_domain = Domain(
            name = domain.name,
            description = domain.description,
            organisation_id = str(domain.organisation_id)
        )
        db.add(db_domain)
        db.commit()
        db.refresh(db_domain)
        return db_domain
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_domain(db: Session, domain_id: str):
    return db.query(Domain).filter(Domain.id == domain_id).first()


def get_all_domains(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Domain).offset(skip).limit(limit).all()


def get_domains_by_organisation(db: Session, organisation_id: str):
    return db.query(Domain).filter(Domain.organisation_id == organisation_id).all()


def update_domain(db: Session, domain_id: str, updates: DomainUpdate):
    db_domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not db_domain:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_domain, field, value)
    db.commit()
    db.refresh(db_domain)
    return db_domain


def delete_domain(db: Session, domain_id: str):
    db_domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not db_domain:
        return None
    db.delete(db_domain)
    db.commit()
    return db_domain