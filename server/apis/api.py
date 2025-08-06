from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import api as api_crud
from ..schemas.api import APICreate, APIUpdate, APIOut

router = APIRouter(prefix="/apis", tags=["APIs"])

@router.post("/", response_model=APIOut)
def create_api(api: APICreate, group_id: str, db: Session = Depends(get_db)):
    return api_crud.create_api(db, group_id, api)



@router.get("/", response_model=list[APIOut])
def list_apis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return api_crud.get_all_apis(db, skip=skip, limit=limit)

@router.get("/by-group/{group_id}", response_model=list[APIOut])
def get_all_apis_by_group(group_id: str, db: Session = Depends(get_db)):
    return api_crud.get_all_by_group_id(db, group_id)


@router.get("/{api_id}", response_model=APIOut)
def read_api(api_id: str, db: Session = Depends(get_db)):
    db_api = api_crud.get_api(db, api_id)
    if not db_api:
        raise HTTPException(status_code=404, detail="API not found")
    return db_api

@router.put("/{api_id}", response_model=APIOut)
def update_api(api_id: str, updates: APIUpdate, db: Session = Depends(get_db)):
    updated = api_crud.update_api(db, api_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="API not found")
    return updated

@router.delete("/{api_id}", response_model=APIOut)
def delete_api(api_id: str, db: Session = Depends(get_db)):
    deleted = api_crud.delete_api(db, api_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="API not found")
    return deleted
