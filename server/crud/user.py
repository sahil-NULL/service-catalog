from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..crud import group_user

# 🔹 Create a new user
def create_user(db: Session, user_data: UserCreate):
    try:
        # Create a new user instance
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password  # In a real app, you would hash this password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 Get a user by ID
def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

# 🔹 Get a user by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# 🔹 Get all users
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_all_by_group_id(db: Session, group_id: str):
    # Step 1: Get user IDs linked to the group
    data = group_user.get_users_by_group(db, group_id)
    user_ids = data["user_ids"]

    if not user_ids:
        return []

    # Step 2: Batch query all users
    users = db.query(User).filter(User.id.in_(user_ids)).all()

    return users

# 🔹 Update a user
def update_user(db: Session, user_id: str, updates: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# 🔹 Delete a user
def delete_user(db: Session, user_id: str):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user