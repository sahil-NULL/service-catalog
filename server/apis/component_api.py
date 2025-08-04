from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.component_api import ComponentAPICreate, ComponentAPIOut
from ..crud import component_api
from ..database import get_db
from uuid import UUID

router = APIRouter(prefix="/component-api", tags=["Component ↔ API Links"])

# 🔹 POST: Create new link
@router.post("/", response_model=ComponentAPIOut)
def link_api_to_component(link: ComponentAPICreate, db: Session = Depends(get_db)):
    return component_api.create_component_api(db, link)

# 🔹 GET: All APIs for a component
@router.get("/{component_id}", response_model=list[ComponentAPIOut])
def get_apis_for_component(component_id: str, db: Session = Depends(get_db)):
    links = component_api.get_apis_by_component(db, component_id)
    return links

# 🔹 DELETE: Unlink API from component
@router.delete("/", response_model=ComponentAPIOut)
def unlink_api_from_component(component_id: str, api_id: str, db: Session = Depends(get_db)):
    link = component_api.delete_component_api(db, component_id, api_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link
