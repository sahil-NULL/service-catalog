# crud/system_component.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.system_component import SystemComponent
from ..schemas.system_component import SystemComponentCreate, SystemComponentOut
from ..models.group_system import group_systems
from ..models.group_component import group_components
from sqlalchemy import select, insert, and_


def create_system_component(db: Session, link: SystemComponentCreate):
    # Step 1: Check if system-component link already exists
    exists = db.execute(
        select(SystemComponent).where(
            (SystemComponent.system_id == str(link.system_id)) &
            (SystemComponent.component_id == str(link.component_id))
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Link already exists")

    # Step 2: Create the system-component link
    db.execute(
        insert(SystemComponent).values(
            system_id=str(link.system_id),
            component_id=str(link.component_id),
            type="direct"
        )
    )

    # Step 3: Fetch all group_ids linked to the system
    group_rows = db.execute(
        select(group_systems.c.group_id).where(
            group_systems.c.system_id == str(link.system_id)
        )
    ).fetchall()

    new_links = []
    for row in group_rows:
        group_id = row.group_id

        # Step 4: Check if (group_id, component_id) already exists
        group_component_exists = db.execute(
            select(group_components).where(
                and_(
                    group_components.c.group_id == group_id,
                    group_components.c.component_id == str(link.component_id)
                )
            )
        ).first()

        if not group_component_exists:
            new_links.append({
                "group_id": group_id,
                "component_id": str(link.component_id)
            })

    # Step 5: Batch insert only the new (non-duplicate) links
    if new_links:
        db.execute(insert(group_components).values(new_links))

    db.commit()
    return link


def get_components_by_system(db: Session, system_id: str):
    results = db.execute(
        select(SystemComponent).where(
            SystemComponent.system_id == system_id
        )
    ).scalars().all()
    return [
        SystemComponentOut(system_id=row.system_id, component_id=row.component_id, type=row.type)
        for row in results
    ]


def delete_system_component(db: Session, system_id: str, component_id: str):
    link = db.query(SystemComponent).filter_by(system_id=system_id, component_id=component_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    db.delete(link)
    db.commit()
    
    return {"message": "Deleted"}
