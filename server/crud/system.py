from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..models.group_component import group_components
from ..models.system_component import SystemComponent
from ..models.component import Component
from ..models.system import System
from ..schemas.system import SystemCreate, SystemUpdate
from ..models.group import Group
from ..schemas.group_system import GroupSystemCreate
from ..crud import group_system, group_user
from fastapi import HTTPException   


def get_all(db: Session):
    return db.query(System).all()


def get_by_id(db: Session, system_id: str):
    return db.query(System).filter(System.id == system_id).first()


def get_all_by_group_id(db: Session, group_id: str):
    # Step 1: Get system IDs linked to the group
    data = group_system.get_systems_by_group(db, group_id)
    system_ids = data["system_ids"]

    if not system_ids:
        return []

    # Step 2: Batch query all systems
    systems = db.query(System).filter(System.id.in_(system_ids)).all()

    return systems


def get_all_addable_components_by_user_id(db: Session, user_id: str, organisation_id: str, system_id: str):
    # Step 1: Get all groups of the user in the organisation
    groups = group_user.get_groups_by_user_and_organisation(db, user_id, organisation_id)
    group_ids = [str(group.id) for group in groups]

    if not group_ids:
        return []

    # Step 2: Get all components available in the user's groups (from group_components)
    group_component_rows = db.execute(
        select(group_components.c.component_id).where(
            group_components.c.group_id.in_(group_ids)
        )
    ).fetchall()

    group_component_ids = {row.component_id for row in group_component_rows}

    if not group_component_ids:
        return []

    # Step 3: Get all components already linked to the system
    system_component_rows = db.execute(
        select(SystemComponent.component_id).where(
            SystemComponent.system_id == system_id
        )
    ).fetchall()

    system_component_ids = {row.component_id for row in system_component_rows}

    # Step 4: Filter out components already in the system
    addable_component_ids = list(group_component_ids - system_component_ids)

    if not addable_component_ids:
        return []

    # Step 5: Fetch component objects
    components = db.query(Component).filter(Component.id.in_(addable_component_ids)).all()

    return components


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
