from uuid import UUID
from sqlalchemy.orm import Session
from ..models.component import Component
from ..schemas.component import ComponentCreate, ComponentUpdate


def get_all(db: Session):
    return db.query(Component).all()


def get_by_id(db: Session, component_id: str):
    return db.query(Component).filter(Component.id == component_id).first()


def create(db: Session, component_data: ComponentCreate):
    new_component = Component(
        name=component_data.name,   
        type=component_data.type,
        description=component_data.description,
        organisation_id=str(component_data.organisation_id)
    )
    db.add(new_component)
    db.commit()
    db.refresh(new_component)
    return new_component


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
