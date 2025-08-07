from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.system import SystemCreate, SystemOut, SystemUpdate
from ..crud import system as system_crud
from ..schemas.component import ComponentOut


router = APIRouter(prefix="/systems", tags=["Systems"])


@router.get("/", response_model=list[SystemOut])
def get_all_systems(db: Session = Depends(get_db)):
    return system_crud.get_all(db)


@router.get("/by-group/{group_id}", response_model=list[SystemOut])
def get_all_systems_by_group(group_id: str, db: Session = Depends(get_db)):
    return system_crud.get_all_by_group_id(db, group_id)


@router.get("/addable-components/", response_model=list[ComponentOut])
def get_all_addable_components_by_user_id(user_id: str, organisation_id: str, system_id: str, db: Session = Depends(get_db)):
    return system_crud.get_all_addable_components_by_user_id(db, user_id, organisation_id, system_id)


@router.get("/{system_id}", response_model=SystemOut)
def get_system(system_id: str, db: Session = Depends(get_db)):
    system = system_crud.get_by_id(db, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return system


@router.post("/", response_model=SystemOut, status_code=status.HTTP_201_CREATED)
def create_system(system: SystemCreate, group_id: str, db: Session = Depends(get_db)):
    return system_crud.create(db, group_id, system)


@router.put("/{system_id}", response_model=SystemOut)
def update_system(system_id: str, system: SystemUpdate, db: Session = Depends(get_db)):
    updated = system_crud.update(db, system_id, system)
    if not updated:
        raise HTTPException(status_code=404, detail="System not found")
    return updated


@router.delete("/{system_id}", response_model=SystemOut)
def delete_system(system_id: str, db: Session = Depends(get_db)):
    deleted = system_crud.delete(db, system_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="System not found")
    return deleted
