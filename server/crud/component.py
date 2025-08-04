from uuid import UUID
from sqlalchemy.orm import Session
from ..models.component import Component
from ..schemas.component import ComponentCreate, ComponentUpdate
from ..models.group import Group
from ..schemas.group_component import GroupComponentCreate
from ..crud import group_component
from fastapi import HTTPException


def get_all(db: Session):
    return db.query(Component).all()


def get_by_id(db: Session, component_id: str):
    return db.query(Component).filter(Component.id == component_id).first()


def create(db: Session, group_id: str | None, component_data: ComponentCreate):
    try:
        # Step 1: Create the component
        new_component = Component(
            name=component_data.name,   
            type=component_data.type,
            description=component_data.description,
            organisation_id=str(component_data.organisation_id)
        )
        db.add(new_component)
        db.commit()
        db.refresh(new_component)

        # Step 2: Determine which group to link to
        final_group_id = group_id
        if final_group_id is None:
            all_teams_group = db.query(Group).filter(
                Group.organisation_id == str(component_data.organisation_id),
                Group.name == "All Teams"
            ).first()
            if not all_teams_group:
                raise HTTPException(status_code=404, detail='"All Teams" group not found')
            final_group_id = str(all_teams_group.id)

        # Step 3: Link the component to the group
        group_component.create_group_component(db, GroupComponentCreate(
            group_id=final_group_id,
            component_id=str(new_component.id)
        ))

        return new_component
    except Exception as e:
        db.rollback()
        raise e


def update(db: Session, component_id: str, updates: ComponentUpdate):
    db_component = db.query(Component).filter(Component.id == component_id).first()
    if not db_component:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_component, field, value)
    db.commit()
    db.refresh(db_component)
    return db_component


def delete(db: Session, component_id: str):
    component = get_by_id(db, component_id)
    if component:
        db.delete(component)
        db.commit()
    return component
