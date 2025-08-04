# routers/group_resource.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.group_resource import GroupResourceCreate, GroupResourceOut
from ..crud import group_resource

router = APIRouter(prefix="/group-resource", tags=["Group ↔ Resource Links"])


@router.post("/", response_model=GroupResourceOut)
def link_resource_to_group(link: GroupResourceCreate, db: Session = Depends(get_db)):
    return group_resource.create_group_resource(db, link)   


@router.get("/{group_id}", response_model=list[GroupResourceOut])
def get_resources_for_group(group_id: str, db: Session = Depends(get_db)):
    return group_resource.get_resources_by_group(db, group_id)


@router.delete("/", response_model=dict)
def unlink_resource_from_group(group_id: str, resource_id: str, db: Session = Depends(get_db)):
    return group_resource.delete_group_resource(db, group_id, resource_id)
