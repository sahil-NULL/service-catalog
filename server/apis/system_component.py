# routers/system_component.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.system_component import SystemComponentCreate, SystemComponentOut
from ..crud import system_component

router = APIRouter(prefix="/system-component", tags=["System ↔ Component Links"])


@router.post("/", response_model=SystemComponentOut)
def link_component_to_system(link: SystemComponentCreate, db: Session = Depends(get_db)):
    return system_component.create_system_component(db, link)


@router.get("/{system_id}", response_model=list[SystemComponentOut])
def get_components_for_system(system_id: str, db: Session = Depends(get_db)):
    return system_component.get_components_by_system(db, system_id)


@router.delete("/", response_model=dict)
def unlink_component_from_system(system_id: str, component_id: str, db: Session = Depends(get_db)):
    return system_component.delete_system_component(db, system_id, component_id)
