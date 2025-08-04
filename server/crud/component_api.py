from sqlalchemy.orm import Session
from ..models.component_api import ComponentAPI
from ..schemas.component_api import ComponentAPICreate, ComponentAPIOut
from sqlalchemy import func
from sqlalchemy import select, insert
from ..models.group_api import group_apis
from ..models.group_component import group_components

# 🔹 Create a new component-api link
def create_component_api(db: Session, link_data: ComponentAPICreate):
    # Step 1: Create the component-api link
    db_link = ComponentAPI(
        component_id=str(link_data.component_id),
        api_id=str(link_data.api_id),
        role=link_data.role
    )
    db.add(db_link)

    # Step 2: Get all group_ids the component belongs to
    group_rows = db.execute(
        select(group_components.c.group_id).where(
            group_components.c.component_id == str(link_data.component_id)
        )
    ).fetchall()
    group_ids = [row.group_id for row in group_rows]

    # Step 3: Get existing group-api links to avoid duplicates
    existing_links = db.execute(
        select(group_apis.c.group_id, group_apis.c.api_id).where(
            group_apis.c.api_id == str(link_data.api_id),
            group_apis.c.group_id.in_(group_ids)
        )
    ).fetchall()
    existing_pairs = {(row.group_id, row.api_id) for row in existing_links}

    # Step 4: Create new group-api links
    new_links = [
        {"group_id": gid, "api_id": str(link_data.api_id)}
        for gid in group_ids
        if (gid, str(link_data.api_id)) not in existing_pairs
    ]

    if new_links:
        db.execute(insert(group_apis), new_links)

    # Step 5: Commit
    db.commit()
    db.refresh(db_link)

    print("Incoming UUIDs:", link_data.component_id, type(link_data.component_id))
    return db_link

# 🔹 Get all API links for a component
def get_apis_by_component(db: Session, component_id: str):
    return db.query(ComponentAPI).filter(ComponentAPI.component_id == component_id).all()

# 🔹 Delete a specific component-api link
def delete_component_api(db: Session, component_id: str, api_id: str):
    link = db.query(ComponentAPI).filter(
        ComponentAPI.component_id == component_id,
        ComponentAPI.api_id == api_id
    ).first()
    if link:
        db.delete(link)
        db.commit()
    return link