from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..crud import graph as crud
from ..database import get_db

router = APIRouter(prefix="/graph", tags=["Graph"])

@router.get("/system/{system_id}")
def get_graph(system_id: str, db: Session = Depends(get_db)):
    return crud.get_system_graph_data(db, system_id)


@router.get("/component/{component_id}")
def get_component_graph(component_id: str, db: Session = Depends(get_db)):
    return crud.get_component_graph_data(db, component_id)