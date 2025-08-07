from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from ..models.group import Group
from ..schemas.group import GroupCreate, GroupUpdate

# 🔹 Create a new group
def create_group(db: Session, group_data: GroupCreate):
    try:
        # If parent_group_id is not provided, set it to "All Teams" group of the same org
        parent_group_id = None

        if group_data.parent_group_id is not None:
            parent_group_id = str(group_data.parent_group_id)
        else:
            # Find the "All Teams" group for the organisation
            all_teams_group = db.query(Group).filter(
                Group.organisation_id == str(group_data.organisation_id),
                Group.name == "All Teams"
            ).first()

            if not all_teams_group:
                raise HTTPException(
                    status_code=404,
                    detail=f'"All Teams" group not found for organisation {group_data.organisation_id}'
                )

            parent_group_id = str(all_teams_group.id)

        # Create the new group
        db_group = Group(
            name=group_data.name,
            parent_group_id=parent_group_id,
            organisation_id=str(group_data.organisation_id)
        )
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        return db_group

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 Get a group by ID
def get_group(db: Session, group_id: str):
    return db.query(Group).filter(Group.id == group_id).first()

# 🔹 Get a group by name
def get_group_by_name(db: Session, name: str):
    return db.query(Group).filter(Group.name == name).first()

# 🔹 Get all groups
def get_all_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Group).offset(skip).limit(limit).all()

# 🔹 Get groups by organisation ID
def get_groups_by_organisation(db: Session, organisation_id: str, skip: int = 0, limit: int = 100):
    return db.query(Group).filter(Group.organisation_id == organisation_id).offset(skip).limit(limit).all()

# 🔹 Update a group
def update_group(db: Session, group_id: str, updates: GroupUpdate):
    db_group = get_group(db, group_id)
    if not db_group:
        return None
    
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_group, field, value)
    
    db.commit()
    db.refresh(db_group)
    return db_group

# 🔹 Delete a group
def delete_group(db: Session, group_id: str):
    db_group = get_group(db, group_id)
    if not db_group:
        return None
    
    db.delete(db_group)
    db.commit()
    return db_group
