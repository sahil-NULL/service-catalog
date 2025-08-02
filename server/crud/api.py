from sqlalchemy.orm import Session
from ..models.api import API
from ..schemas.api import APICreate, APIUpdate

def create_api(db: Session, api_data: APICreate):
    new_api = API(
        name=api_data.name,
        type=api_data.type,
        description=api_data.description,
        organisation_id=str(api_data.organisation_id),
    )
    db.add(new_api)
    db.commit()
    db.refresh(new_api)
    return new_api

def get_api(db: Session, api_id: str):
    return db.query(API).filter(API.id == api_id).first()

def get_all_apis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(API).offset(skip).limit(limit).all()

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
