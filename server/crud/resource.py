from sqlalchemy.orm import Session
from ..models.resource import Resource
from ..schemas.resource import ResourceCreate, ResourceUpdate
from ..models.group import Group
from ..schemas.group_resource import GroupResourceCreate
from ..crud import group_resource
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
