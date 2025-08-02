from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.system import SystemCreate, SystemOut, SystemUpdate
from ..crud import system as system_crud


router = APIRouter(prefix="/systems", tags=["Systems"])


@router.get("/", response_model=list[SystemOut])
def get_all_systems(db: Session = Depends(get_db)):
    return system_crud.get_all(db)


@router.get("/{system_id}", response_model=SystemOut)
def get_system(system_id: str, db: Session = Depends(get_db)):
    system = system_crud.get_by_id(db, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return system


@router.post("/", response_model=SystemOut, status_code=status.HTTP_201_CREATED)
def create_system(system: SystemCreate, db: Session = Depends(get_db)):
    return system_crud.create(db, system)


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
