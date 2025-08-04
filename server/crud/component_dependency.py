# crud/component_dependency.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.component_dependency import ComponentDependency
from ..schemas.component_dependency import ComponentDependencyCreate
from ..models.group_component import group_components
from sqlalchemy import select, insert
from ..models.system_component import SystemComponent


def create_dependency(db: Session, link: ComponentDependencyCreate):
    # Step 1: Check if dependency already exists
    existing = db.query(ComponentDependency).filter_by(
        source_component_id=str(link.source_component_id),
        target_component_id=str(link.target_component_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Dependency already exists")

    # Step 2: Add new dependency
    db_link = ComponentDependency(
        source_component_id=str(link.source_component_id),
        target_component_id=str(link.target_component_id),
    )
    db.add(db_link)

    target_component_id = str(link.target_component_id)

    # Step 3: Get all groups the source component belongs to
    source_group_rows = db.execute(
        select(group_components.c.group_id).where(
            group_components.c.component_id == str(link.source_component_id)
        )
    ).fetchall()

    # Step 4: Add target component to same groups
    new_group_links = []
    for row in source_group_rows:
        group_id = row.group_id
        exists = db.execute(
            select(group_components).where(
                (group_components.c.group_id == group_id) &
                (group_components.c.component_id == target_component_id)
            )
        ).first()
        if not exists:
            new_group_links.append({
                "group_id": group_id,
                "component_id": target_component_id
            })

    if new_group_links:
        db.execute(insert(group_components).values(new_group_links))

    # Step 5: Get all systems the source component belongs to
    source_system_rows = db.execute(
        select(SystemComponent.system_id).where(
            SystemComponent.component_id == str(link.source_component_id)
        )
    ).fetchall()

    # Step 6: Add target component to same systems
    new_system_links = []
    for row in source_system_rows:
        system_id = row.system_id
        exists = db.execute(
            select(SystemComponent).where(
                (SystemComponent.system_id == system_id) &
                (SystemComponent.component_id == target_component_id)
            )
        ).first()
        if not exists:
            new_system_links.append({
                "system_id": system_id,
                "component_id": target_component_id,
                "type": "indirect"
            })

    if new_system_links:
        db.execute(insert(SystemComponent).values(new_system_links))

    db.commit()
    db.refresh(db_link)
    return db_link


def get_dependencies_for_component(db: Session, component_id: str):
    return db.query(ComponentDependency).filter_by(source_component_id=component_id).all()


def get_dependents_of_component(db: Session, component_id: str):
    return db.query(ComponentDependency).filter_by(target_component_id=component_id).all()


def delete_dependency(db: Session, source_id: str, target_id: str):
    link = db.query(ComponentDependency).filter_by(
        source_component_id=str(source_id),
        target_component_id=str(target_id)
    ).first()

    if not link:
        raise HTTPException(status_code=404, detail="Dependency not found")

    db.delete(link)
    db.commit()
    return {"message": "Dependency deleted"}
