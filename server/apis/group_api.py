# routers/group_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.group_api import GroupApiCreate, GroupApiOut
from ..crud import group_api

router = APIRouter(prefix="/group-api", tags=["Group ↔ API Links"])


@router.post("/", response_model=GroupApiOut)
def link_api_to_group(link: GroupApiCreate, db: Session = Depends(get_db)):
    return group_api.create_group_api(db, link)   


@router.get("/{group_id}", response_model=list[GroupApiOut])
def get_apis_for_group(group_id: str, db: Session = Depends(get_db)):
    return group_api.get_apis_by_group(db, group_id)


@router.delete("/", response_model=dict)
def unlink_api_from_group(group_id: str, api_id: str, db: Session = Depends(get_db)):
    return group_api.delete_group_api(db, group_id, api_id) 
