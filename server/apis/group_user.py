# routers/group_user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.group_user import GroupUserCreate, GroupUserOut
from ..crud import group_user

router = APIRouter(prefix="/group-user", tags=["Group ↔ User Links"])


@router.post("/", response_model=GroupUserOut)
def link_user_to_group(link: GroupUserCreate, db: Session = Depends(get_db)):
    return group_user.create_group_user(db, link)


@router.get("/{group_id}", response_model=list[GroupUserOut])
def get_users_for_group(group_id: str, db: Session = Depends(get_db)):
    return group_user.get_users_by_group(db, group_id)


@router.delete("/", response_model=dict)
def unlink_user_from_group(group_id: str, user_id: str, db: Session = Depends(get_db)):
    return group_user.delete_group_user(db, group_id, user_id)
