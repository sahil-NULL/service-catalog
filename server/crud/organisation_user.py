# crud/organisation_user.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.organisation_user import organisation_users
from ..schemas.organisation_user import OrganisationUserCreate, OrganisationUserOut


def create_organisation_user(db: Session, link: OrganisationUserCreate):
    exists = db.execute(
        organisation_users.select().where(
            (organisation_users.c.organisation_id == str(link.organisation_id)) &
            (organisation_users.c.user_id == str(link.user_id))
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Link already exists")

    db.execute(
        organisation_users.insert().values(
            organisation_id=str(link.organisation_id),
            user_id=str(link.user_id)
        )
    )
    db.commit()
    return link


def get_users_by_organisation(db: Session, organisation_id: str):
    rows = db.execute(
        organisation_users.select().where(
            organisation_users.c.organisation_id == organisation_id
        )
    ).fetchall()

    return [
        OrganisationUserOut(organisation_id=row.organisation_id, user_id=row.user_id)
        for row in rows
    ]


def delete_organisation_user(db: Session, organisation_id: str, user_id: str):
    result = db.execute(
        organisation_users.delete().where(
            (organisation_users.c.organisation_id == str(organisation_id)) &
            (organisation_users.c.user_id == str(user_id))
        )
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Link not found")

    return {"message": "Deleted"}
