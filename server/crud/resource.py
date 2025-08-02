from sqlalchemy.orm import Session
from ..models.resource import Resource
from ..schemas.resource import ResourceCreate, ResourceUpdate


def create_resource(db: Session, resource_data: ResourceCreate):
    new_resource = Resource(
        name=resource_data.name,
        type=resource_data.type,
        description=resource_data.description,
        organisation_id=str(resource_data.organisation_id),
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
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
