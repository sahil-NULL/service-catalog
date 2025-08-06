from sqlalchemy.orm import Session
from ..models.api import API
from ..schemas.api import APICreate, APIUpdate
from ..models.group import Group
from ..schemas.group_api import GroupApiCreate
from ..crud import group_api
from fastapi import HTTPException

def create_api(db: Session, group_id: str, api_data: APICreate):
    # Step 1: Create the API
    new_api = API(
        name=api_data.name,
        type=api_data.type,
        description=api_data.description,
        organisation_id=str(api_data.organisation_id),
    )
    db.add(new_api)
    db.commit()
    db.refresh(new_api)
    
    # Step 2: Determine which group to link to
    final_group_id = group_id
    if final_group_id is None:
        all_teams_group = db.query(Group).filter(
            Group.organisation_id == str(api_data.organisation_id),
            Group.name == "All Teams"
        ).first()
        if not all_teams_group:
            raise HTTPException(status_code=404, detail='"All Teams" group not found')
        final_group_id = str(all_teams_group.id)

    # Step 3: Link the API to the group
    group_api.create_group_api(db, GroupApiCreate(
        group_id=final_group_id,
        api_id=str(new_api.id)
    ))
    return new_api

def get_api(db: Session, api_id: str):
    return db.query(API).filter(API.id == api_id).first()

def get_all_apis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(API).offset(skip).limit(limit).all()

def get_all_by_group_id(db: Session, group_id: str):
    # Step 1: Get api IDs linked to the group
    data = group_api.get_apis_by_group(db, group_id)
    api_ids = data["api_ids"]

    if not api_ids:
        return []

    # Step 2: Batch query all apis
    apis = db.query(API).filter(API.id.in_(api_ids)).all()

    return apis

def update_api(db: Session, api_id: str, updates: APIUpdate):
    db_api = db.query(API).filter(API.id == api_id).first()
    if not db_api:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_api, field, value)
    db.commit()
    db.refresh(db_api)
    return db_api

def delete_api(db: Session, api_id: str):
    db_api = db.query(API).filter(API.id == api_id).first()
    if not db_api:
        return None
    db.delete(db_api)
    db.commit()
    return db_api
