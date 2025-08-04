# routers/group_component.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.group_component import GroupComponentCreate, GroupComponentOut
from ..crud import group_component

router = APIRouter(prefix="/group-component", tags=["Group ↔ Component Links"])


@router.post("/", response_model=GroupComponentOut)
def link_component_to_group(link: GroupComponentCreate, db: Session = Depends(get_db)):
    return group_component.create_group_component(db, link)


@router.get("/{group_id}", response_model=list[GroupComponentOut])
def get_components_for_group(group_id: str, db: Session = Depends(get_db)):
    return group_component.get_components_by_group(db, group_id)


@router.delete("/", response_model=dict)
def unlink_component_from_group(group_id: str, component_id: str, db: Session = Depends(get_db)):
    return group_component.delete_group_component(db, group_id, component_id)
