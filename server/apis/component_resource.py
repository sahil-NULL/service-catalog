# routers/component_resource.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.component_resource import ComponentResourceCreate, ComponentResourceOut
from ..crud import component_resource

router = APIRouter(prefix="/component-resource", tags=["Component ↔ Resource Links"])


@router.post("/", response_model=ComponentResourceOut)
def link_resource_to_component(link: ComponentResourceCreate, db: Session = Depends(get_db)):
    return component_resource.create_component_resource(db, link)


@router.get("/{component_id}", response_model=list[ComponentResourceOut])
def get_resources_for_component(component_id: str, db: Session = Depends(get_db)):
    return component_resource.get_resources_by_component(db, component_id)


@router.delete("/", response_model=dict)
def unlink_resource_from_component(component_id: str, resource_id: str, db: Session = Depends(get_db)):
    return component_resource.delete_component_resource(db, component_id, resource_id)
