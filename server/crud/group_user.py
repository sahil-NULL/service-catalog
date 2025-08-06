# crud/group_user.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.group_user import group_users
from ..schemas.group_user import GroupUserCreate, GroupUserOut
from ..models.group import Group
from sqlalchemy import select


def create_group_user(db: Session, link: GroupUserCreate):
    exists = db.execute(
        group_users.select().where(
            (group_users.c.group_id == str(link.group_id)) &
            (group_users.c.user_id == str(link.user_id))
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Link already exists")

    db.execute(
        group_users.insert().values(
            group_id=str(link.group_id),
            user_id=str(link.user_id)
        )
    )
    db.commit()
    return link


def get_users_by_group(db: Session, group_id: str):
    rows = db.execute(
        group_users.select().where(group_users.c.group_id == group_id)
    ).fetchall()

    user_ids = [row.user_id for row in rows]

    return {
        "group_id": group_id,
        "user_ids": user_ids
    }


def get_groups_by_user_and_organisation(db: Session, user_id: str, organisation_id: str):
    # Step 1: Get group_ids where user is a member
    user_group_rows = db.execute(
        select(group_users.c.group_id).where(group_users.c.user_id == user_id)
    ).fetchall()

    user_group_ids = [row.group_id for row in user_group_rows]

    if not user_group_ids:
        return []

    # Step 2: Filter groups by organisation_id and user group ids
    groups = db.query(Group).filter(
        Group.id.in_(user_group_ids),
        Group.organisation_id == organisation_id
    ).all()

    return groups


def delete_group_user(db: Session, group_id: str, user_id: str):
    result = db.execute(
        group_users.delete().where(
            (group_users.c.group_id == str(group_id)) &
            (group_users.c.user_id == str(user_id))
        )
    )
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Link not found")

    return {"message": "Deleted"}
