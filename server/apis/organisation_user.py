# routers/organisation_user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.organisation_user import OrganisationUserCreate, OrganisationUserOut
from ..crud import organisation_user

router = APIRouter(prefix="/organisation-user", tags=["Organisation ↔ User Links"])


@router.post("/", response_model=OrganisationUserOut)
def link_user_to_organisation(link: OrganisationUserCreate, db: Session = Depends(get_db)):
    return organisation_user.create_organisation_user(db, link)


@router.get("/{organisation_id}", response_model=list[OrganisationUserOut])
def get_users_for_organisation(organisation_id: str, db: Session = Depends(get_db)):
    return organisation_user.get_users_by_organisation(db, organisation_id)


@router.delete("/", response_model=dict)
def unlink_user_from_organisation(organisation_id: str, user_id: str, db: Session = Depends(get_db)):
    return organisation_user.delete_organisation_user(db, organisation_id, user_id)
