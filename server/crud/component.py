from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.component_dependency import ComponentDependency
from ..models.component import Component
from ..schemas.component import ComponentCreate, ComponentUpdate
from ..models.group import Group
from ..models.group_component import group_components
from ..schemas.group_component import GroupComponentCreate
from ..crud import group_component, group_user
from fastapi import HTTPException


def get_all(db: Session):
    return db.query(Component).all()


def get_by_id(db: Session, component_id: str):
    return db.query(Component).filter(Component.id == component_id).first()


def get_all_by_group_id(db: Session, group_id: str):
    # Step 1: Get component IDs linked to the group
    data = group_component.get_components_by_group(db, group_id)
    component_ids = data["component_ids"]
    print(component_ids)

    if not component_ids:
        return []

    # Step 2: Batch query all components
    components = db.query(Component).filter(Component.id.in_(component_ids)).all()
    print(components)

    return components


def get_all_addable_components_by_user_id(db: Session, user_id: str, organisation_id: str, component_id: str):
    # Step 1: Get all groups of the user in the organisation
    groups = group_user.get_groups_by_user_and_organisation(db, user_id, organisation_id)
    group_ids = [group.id for group in groups]

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

    # Step 3: Get all components that are already linked to the component
    visited = set()
    stack = [component_id]

    linked_component_ids = set()

    while stack:
        current_id = stack.pop()
        if current_id in visited:
            continue
        visited.add(current_id)
        linked_component_ids.add(current_id)

        # Fetch outgoing dependencies from current component
        deps = db.query(ComponentDependency).filter(
            ComponentDependency.source_component_id == current_id
        ).all()

        for dep in deps:
            if dep.target_component_id not in visited:
                stack.append(dep.target_component_id)

    # Step 4: Filter out components already in the component
    addable_component_ids = list(group_component_ids - linked_component_ids)

    if not addable_component_ids:
        return []

    # Step 5: Fetch component objects
    components = db.query(Component).filter(Component.id.in_(addable_component_ids)).all()

    return components


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
