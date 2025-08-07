from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.resource import Resource
from ..models.group_resource import group_resources
from ..schemas.resource import ResourceCreate, ResourceUpdate
from ..models.group import Group
from ..schemas.group_resource import GroupResourceCreate
from ..crud import group_resource
from ..crud import group_user
from ..crud import component_resource
from fastapi import HTTPException


def create_resource(db: Session, group_id: str, resource_data: ResourceCreate):

    # Step 1: Create the resource
    new_resource = Resource(
        name=resource_data.name,
        type=resource_data.type,
        description=resource_data.description,
        organisation_id=str(resource_data.organisation_id),
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    # Step 2: Determine which group to link to
    final_group_id = group_id
    if final_group_id is None:
        all_teams_group = db.query(Group).filter(
            Group.organisation_id == str(resource_data.organisation_id),
            Group.name == "All Teams"
        ).first()
        if not all_teams_group:
            raise HTTPException(status_code=404, detail='"All Teams" group not found')
        final_group_id = str(all_teams_group.id)

    # Step 3: Link the component to the group
    group_resource.create_group_resource(db, GroupResourceCreate(
        group_id=final_group_id,
        resource_id=str(new_resource.id)
    ))
    return new_resource

def get_resource(db: Session, resource_id: str):
    return db.query(Resource).filter(Resource.id == resource_id).first()

def get_all_by_group_id(db: Session, group_id: str):
    # Step 1: Get resource IDs linked to the group
    data = group_resource.get_resources_by_group(db, group_id)
    resource_ids = data["resource_ids"]

    if not resource_ids:
        return []

    # Step 2: Batch query all resources
    resources = db.query(Resource).filter(Resource.id.in_(resource_ids)).all()

    return resources

def get_all_addable_resources_by_user_id(db: Session, component_id: str, user_id: str, organisation_id: str):
    # Step 1: Get all groups of the user in the organisation
    groups = group_user.get_groups_by_user_and_organisation(db, user_id, organisation_id)
    group_ids = [str(group.id) for group in groups]

    if not group_ids:
        return []

    # Step 2: Get all resources available in the user's groups (from group_resource)
    group_resource_rows = db.execute(
        select(group_resources.c.resource_id).where(
            group_resources.c.group_id.in_(group_ids)
        )
    ).fetchall()

    group_resource_ids = {row.resource_id for row in group_resource_rows}


    if not group_resource_ids:
        return []

    # Step 3: Get all resources already linked to the component
    component_resource_rows = component_resource.get_resources_by_component(db, component_id)
    linked_resource_ids = {row.resource_id for row in component_resource_rows}


    # Step 4: Filter out resources already in the component
    addable_resource_ids = list(group_resource_ids - linked_resource_ids)


    if not addable_resource_ids:
        return []

    # Step 5: Fetch resource objects
    resources = db.query(Resource).filter(Resource.id.in_(addable_resource_ids)).all()

    return resources

def get_all_resources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Resource).offset(skip).limit(limit).all()

def update_resource(db: Session, resource_id: str, updates: ResourceUpdate):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)
    return resource

def delete_resource(db: Session, resource_id: str):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        return None
    db.delete(resource)
    db.commit()
    return resource
