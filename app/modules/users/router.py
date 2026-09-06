import uuid
from fastapi import APIRouter, status, Depends

from .schemas import UserResponse, UserCreate, UserResponseList, UserUpdate
from .dependencies import UserServiceDep, UserQueryDep
from ..auth.dependencies import get_current_admin

router = APIRouter(
    prefix="/user", tags=["User"], dependencies=[Depends(get_current_admin)]
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create(user: UserCreate, service: UserServiceDep):
    return await service.create(user)


@router.get("/", response_model=UserResponseList)
async def find_all(query: UserQueryDep, service: UserServiceDep):
    return await service.find_all(query)


@router.get("/{user_id}", response_model=UserResponse)
async def find_by_id(user_id: uuid.UUID, service: UserServiceDep):
    return await service.find_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update(user_id: uuid.UUID, user_data: UserUpdate, service: UserServiceDep):
    return await service.update(user_id=user_id, user_data=user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: uuid.UUID, service: UserServiceDep):
    return await service.delete(user_id)
