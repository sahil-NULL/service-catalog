# crud/domain_system.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.domain_system import domain_systems
from ..schemas.domain_system import DomainSystemCreate, DomainSystemOut


def create_domain_system(db: Session, link: DomainSystemCreate):
    exists = db.execute(
        domain_systems.select().where(
            (domain_systems.c.domain_id == str(link.domain_id)) &
            (domain_systems.c.system_id == str(link.system_id))
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Link already exists")

    db.execute(
        domain_systems.insert().values(
            domain_id=str(link.domain_id),
            system_id=str(link.system_id)
        )
    )
    db.commit()
    return link


def get_systems_by_domain(db: Session, domain_id: str):
    rows = db.execute(
        domain_systems.select().where(
            domain_systems.c.domain_id == domain_id
        )
    ).fetchall()

    return [
        DomainSystemOut(domain_id=row.domain_id, system_id=row.system_id)
        for row in rows
    ]


def delete_domain_system(db: Session, domain_id: str, system_id: str):
    result = db.execute(
        domain_systems.delete().where(
            (domain_systems.c.domain_id == domain_id) &
            (domain_systems.c.system_id == system_id)
        )
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Link not found")
    
    return {"message": "Deleted"}
