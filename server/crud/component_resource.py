# crud/component_resource.py
from sqlalchemy.orm import Session
from ..models.component_resource import component_resources
from ..schemas.component_resource import ComponentResourceCreate, ComponentResourceOut
from fastapi import HTTPException
from sqlalchemy import select, insert
from ..models.group_resource import group_resources
from ..models.group_component import group_components


def create_component_resource(db: Session, link: ComponentResourceCreate):
    # Step 1: Check if component-resource link already exists
    exists = db.execute(
        component_resources.select().where(
            (component_resources.c.component_id == str(link.component_id)) &
            (component_resources.c.resource_id == str(link.resource_id))
        )
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Link already exists")

    # Step 2: Insert the component-resource link
    db.execute(
        component_resources.insert().values(
            component_id=str(link.component_id),
            resource_id=str(link.resource_id)
        )
    )

    # Step 3: Get all groups the component is linked to
    component_group_rows = db.execute(
        select(group_components.c.group_id).where(
            group_components.c.component_id == str(link.component_id)
        )
    ).fetchall()
    group_ids = [row.group_id for row in component_group_rows]

    # Step 4: Prevent duplicate group-resource links
    existing_links = db.execute(
        select(group_resources.c.group_id, group_resources.c.resource_id).where(
            group_resources.c.resource_id == str(link.resource_id),
            group_resources.c.group_id.in_(group_ids)
        )
    ).fetchall()
    existing_pairs = {(row.group_id, row.resource_id) for row in existing_links}

    # Step 5: Create new group-resource links only if not already present
    new_links = [
        {"group_id": gid, "resource_id": str(link.resource_id)}
        for gid in group_ids
        if (gid, str(link.resource_id)) not in existing_pairs
    ]

    if new_links:
        db.execute(insert(group_resources), new_links)

    # Step 6: Commit and return response
    db.commit()
    return link


def get_resources_by_component(db: Session, component_id: str):
    results = db.execute(
        component_resources.select().where(
            component_resources.c.component_id == component_id
        )
    ).fetchall()
    return [
        ComponentResourceOut(component_id=row.component_id, resource_id=row.resource_id)
        for row in results
    ]


def delete_component_resource(db: Session, component_id: str, resource_id: str):
    result = db.execute(
        component_resources.delete().where(
            (component_resources.c.component_id == component_id) &
            (component_resources.c.resource_id == resource_id)
        )
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"message": "Deleted"}
