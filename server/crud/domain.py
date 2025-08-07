from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from uuid import UUID
from ..models.domain import Domain
from ..models.group_system import group_systems
from ..schemas.domain import *
from ..crud import group_user
from ..crud import domain_system
from ..models.system import System


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


def get_addable_systems_by_user_id(db: Session, user_id: str, organisation_id: str, domain_id: str):
    # Step 1: Get all groups of the user in the organisation
    groups = group_user.get_groups_by_user_and_organisation(db, user_id, organisation_id)
    group_ids = [str(group.id) for group in groups]

    # Step 2: Get all systems available in the user's groups (from group_systems)
    group_system_rows = db.execute(
        select(group_systems.c.system_id).where(
            group_systems.c.group_id.in_(group_ids)
        )
    ).fetchall()

    all_system_ids = [row.system_id for row in group_system_rows]

    # Step 3: Get all systems linked to the domain
    domain_systems = domain_system.get_systems_by_domain(db, domain_id)
    linked_system_ids = [row.system_id for row in domain_systems]

    # Step 4: Filter out systems that are already linked to the domain
    addable_system_ids = list(set(all_system_ids) - set(linked_system_ids))

    # Step 5: Get all systems by IDs
    addable_systems = db.query(System).filter(System.id.in_(addable_system_ids)).all()

    return addable_systems


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
