from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..crud import user as user_crud
from ..schemas.user import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    db_user = user_crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    return user_crud.create_user(db, user)

# @router.get("/{user_id}", response_model=UserOut)
# def read_user(user_id: str, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_all_users(db, skip=skip, limit=limit)
    return users

@router.get("/{group_id}", response_model=List[UserOut])
def get_all_users_by_group(group_id: str, db: Session = Depends(get_db)):
    return user_crud.get_all_by_group_id(db, group_id)

@router.get("/addable/{group_id}", response_model=List[UserOut])
def get_addable_users_for_group(group_id: str, db: Session = Depends(get_db)):
    return user_crud.get_all_addable_users_for_group(db, group_id)

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = user_crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    deleted_user = user_crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user