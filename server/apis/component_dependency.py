# routers/component_dependency.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.component_dependency import ComponentDependencyCreate, ComponentDependencyOut
from ..crud import component_dependency

router = APIRouter(prefix="/component-dependency", tags=["Component ↔ Component Dependencies"])


@router.post("/", response_model=ComponentDependencyOut)
def create_component_dependency(link: ComponentDependencyCreate, db: Session = Depends(get_db)):
    return component_dependency.create_dependency(db, link)


@router.get("/depends-on/{component_id}", response_model=list[ComponentDependencyOut])
def get_dependencies(component_id: str, db: Session = Depends(get_db)):
    return component_dependency.get_dependencies_for_component(db, component_id)


@router.get("/dependents/{component_id}", response_model=list[ComponentDependencyOut])
def get_dependents(component_id: str, db: Session = Depends(get_db)):
    return component_dependency.get_dependents_of_component(db, component_id)


@router.delete("/", response_model=dict)
def delete_dependency(source_id: str, target_id: str, db: Session = Depends(get_db)):
    return component_dependency.delete_dependency(db, source_id, target_id)
