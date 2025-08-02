from sqlalchemy.orm import Session
from ..schemas.organisation import OrganisationCreate, OrganisationUpdate
from ..models.organisation import Organisation
from uuid import UUID
from fastapi import HTTPException

# 🔹 Create a new organisation
def create_organisation(db: Session, org_data: OrganisationCreate) -> Organisation:
    try:
        org = Organisation(**org_data.model_dump())
        db.add(org)
        db.commit()
        db.refresh(org)
        return org
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 Get one organisation by ID
def get_organisation(db: Session, org_id: str) -> Organisation:
    return db.query(Organisation).filter(Organisation.id == org_id).first()

# 🔹 Get all organisations
def get_all_organisations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Organisation).offset(skip).limit(limit).all()

# 🔹 Update an organisation
def update_organisation(db: Session, org_id: str, updates: OrganisationUpdate):
    org = get_organisation(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(org, key, value)
    db.commit()
    db.refresh(org)
    return org

# 🔹 Delete an organisation
def delete_organisation(db: Session, org_id: str):
    org = get_organisation(db, org_id)  
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")   
    
    db.delete(org)
    db.commit()
    return org
