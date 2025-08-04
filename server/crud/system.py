from uuid import UUID
from sqlalchemy.orm import Session
from ..models.system import System
from ..schemas.system import SystemCreate, SystemUpdate
from ..models.group import Group
from ..schemas.group_system import GroupSystemCreate
from ..crud import group_system
from fastapi import HTTPException


def get_all(db: Session):
    return db.query(System).all()


def get_by_id(db: Session, system_id: str):
    return db.query(System).filter(System.id == system_id).first()


def create(db: Session, group_id: str | None, system_data: SystemCreate):
    try:
        # Step 1: Create the system
        new_system = System(
            name=system_data.name,
            description=system_data.description,
            organisation_id=str(system_data.organisation_id)
        )
        db.add(new_system)
        db.commit()
        db.refresh(new_system)

        # Step 2: Determine which group to link to
        final_group_id = group_id
        if final_group_id is None:
            all_teams_group = db.query(Group).filter(
                Group.organisation_id == str(system_data.organisation_id),
                Group.name == "All Teams"
            ).first()
            if not all_teams_group:
                raise HTTPException(status_code=404, detail='"All Teams" group not found')
            final_group_id = str(all_teams_group.id)

        # Step 3: Create system-group link using shared CRUD logic
        group_system.create_group_system(db, GroupSystemCreate(
            group_id=final_group_id,
            system_id=str(new_system.id)
        ))

        return new_system

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def update(db: Session, system_id: str, updates: SystemUpdate):
    db_system = db.query(System).filter(System.id == system_id).first()
    if not db_system:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_system, field, value)
    db.commit()
    db.refresh(db_system)
    return db_system


def delete(db: Session, system_id: str):
    system = get_by_id(db, system_id)
    if system:
        db.delete(system)
        db.commit()
    return system
