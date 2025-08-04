# crud/group_user.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.group_user import group_users
from ..schemas.group_user import GroupUserCreate, GroupUserOut


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

    return [
        GroupUserOut(group_id=row.group_id, user_id=row.user_id)
        for row in rows
    ]


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
