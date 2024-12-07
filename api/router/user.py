from fastapi import APIRouter, HTTPException
from api.schemas import UserBase, UserDisplay
from ..db.postgres import postgre_db
from typing import List

user_router = APIRouter(
    prefix='/user',
    tags=['user']
)

@user_router.post('/', response_model=UserDisplay)
def create_user(user: UserBase):
    return  postgre_db.create_user(user)

@user_router.get('/', response_model=List[UserDisplay])
def get_all_users():
    return postgre_db.get_all_users()

@user_router.get('/{id}', response_model=UserDisplay)
def get_user(id: int):
    return postgre_db.get_user(id)

@user_router.post('/{id}/update')
def update_user(id: int, new_user: UserBase):
    return postgre_db.update_user(id, new_user)

@user_router.get('/{id}/delete')
def delete_user(id: int):
    return postgre_db.delete_user(id)