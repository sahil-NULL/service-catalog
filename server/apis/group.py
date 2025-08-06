from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..crud import group as group_crud
from ..schemas.group import GroupCreate, GroupUpdate, GroupOut

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.post("/", response_model=GroupOut, status_code=status.HTTP_201_CREATED)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    # Check if a group with the same name exists in the same organisation
    db_group = group_crud.get_group_by_name(db, group.name)
    if db_group and str(db_group.organisation_id) == str(group.organisation_id):
        raise HTTPException(
            status_code=400,
            detail="Group with this name already exists in the organisation"
        )
    return group_crud.create_group(db, group)

@router.get("/group/{group_id}", response_model=GroupOut)
def read_group(group_id: str, db: Session = Depends(get_db)):
    db_group = group_crud.get_group(db, group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.get("/", response_model=List[GroupOut])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = group_crud.get_all_groups(db, skip=skip, limit=limit)
    return groups

@router.get("/organisation/{organisation_id}", response_model=List[GroupOut])
def read_groups_by_organisation(organisation_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = group_crud.get_groups_by_organisation(db, organisation_id, skip=skip, limit=limit)
    return groups

@router.put("/{group_id}", response_model=GroupOut)
def update_group(group_id: str, group: GroupUpdate, db: Session = Depends(get_db)):
    updated_group = group_crud.update_group(db, group_id, group)
    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated_group

@router.delete("/{group_id}", response_model=GroupOut)
def delete_group(group_id: str, db: Session = Depends(get_db)):
    deleted_group = group_crud.delete_group(db, group_id)
    if not deleted_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return deleted_group