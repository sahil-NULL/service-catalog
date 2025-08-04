# routers/resource.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud import resource as resource_crud
from ..schemas.resource import ResourceCreate, ResourceUpdate, ResourceOut
from ..database import get_db

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.post("/", response_model=ResourceOut)
def create_resource(group_id: str, resource: ResourceCreate, db: Session = Depends(get_db)):
    return resource_crud.create_resource(db, group_id, resource)

@router.get("/{resource_id}", response_model=ResourceOut)
def read_resource(resource_id: str, db: Session = Depends(get_db)):
    db_resource = resource_crud.get_resource(db, resource_id)
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@router.get("/", response_model=list[ResourceOut])
def list_resources(db: Session = Depends(get_db)):
    return resource_crud.get_all_resources(db)

@router.put("/{resource_id}", response_model=ResourceOut)
def update_resource(resource_id: str, updates: ResourceUpdate, db: Session = Depends(get_db)):
    updated = resource_crud.update_resource(db, resource_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Resource not found")
    return updated

@router.delete("/{resource_id}", response_model=ResourceOut)
def delete_resource(resource_id: str, db: Session = Depends(get_db)):
    deleted = resource_crud.delete_resource(db, resource_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Resource not found")
    return deleted
