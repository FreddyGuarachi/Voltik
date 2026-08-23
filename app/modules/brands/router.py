import uuid
from fastapi import APIRouter, status

from .schemas import BrandCreate, BrandResponse, BrandResponseList, BrandUpdate
from .dependencies import BrandServiceDep, BrandQueryDep

router = APIRouter(prefix="/brand", tags=["Brand"])


@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create(brand: BrandCreate, service: BrandServiceDep):
    return await service.create(brand)


@router.get("/", response_model=BrandResponseList)
async def find_all(query: BrandQueryDep, service: BrandServiceDep):
    return await service.find_all(query)


@router.get("/{brand_id}", response_model=BrandResponse)
async def find_by_id(brand_id: uuid.UUID, service: BrandServiceDep):
    return await service.find_by_id(brand_id)


@router.put("/{brand_id}", response_model=BrandResponse)
async def update(
    brand_id: uuid.UUID, brand_data: BrandUpdate, service: BrandServiceDep
):
    return await service.update(brand_id=brand_id, brand_data=brand_data)


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(brand_id: uuid.UUID, service: BrandServiceDep):
    return await service.delete(brand_id)
