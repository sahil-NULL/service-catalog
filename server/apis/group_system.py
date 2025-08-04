# routers/group_system.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.group_system import GroupSystemCreate, GroupSystemOut
from ..crud import group_system

router = APIRouter(prefix="/group-system", tags=["Group ↔ System Links"])


@router.post("/", response_model=GroupSystemOut)
def link_system_to_group(link: GroupSystemCreate, db: Session = Depends(get_db)):
    return group_system.create_group_system(db, link)


@router.get("/{group_id}", response_model=list[GroupSystemOut])
def get_systems_for_group(group_id: str, db: Session = Depends(get_db)):
    return group_system.get_systems_by_group(db, group_id)


@router.delete("/", response_model=dict)
def unlink_system_from_group(group_id: str, system_id: str, db: Session = Depends(get_db)):
    return group_system.delete_group_system(db, group_id, system_id)
