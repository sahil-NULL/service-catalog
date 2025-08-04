from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.component import ComponentCreate, ComponentOut, ComponentUpdate
from ..crud import component as component_crud


router = APIRouter(prefix="/components", tags=["Components"])


@router.get("/", response_model=list[ComponentOut])
def get_all_components(db: Session = Depends(get_db)):
    return component_crud.get_all(db)


@router.get("/{component_id}", response_model=ComponentOut)
def get_component(component_id: str, db: Session = Depends(get_db)):
    component = component_crud.get_by_id(db, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return component


@router.post("/", response_model=ComponentOut, status_code=status.HTTP_201_CREATED)
def create_component(component: ComponentCreate, group_id: str, db: Session = Depends(get_db)):
    return component_crud.create(db, group_id, component)


@router.put("/{component_id}", response_model=ComponentOut)
def update_component(component_id: str, component: ComponentUpdate, db: Session = Depends(get_db)):
    updated = component_crud.update(db, component_id, component)
    if not updated:
        raise HTTPException(status_code=404, detail="Component not found")
    return updated


@router.delete("/{component_id}", response_model=ComponentOut)
def delete_component(component_id: str, db: Session = Depends(get_db)):
    deleted = component_crud.delete(db, component_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Component not found")
    return deleted
