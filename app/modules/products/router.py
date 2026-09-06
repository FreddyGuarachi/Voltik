import uuid
from fastapi import APIRouter, status, Depends

from .dependencies import ProductServiceDep, ProductQueryDep
from .schemas import ProductResponse, ProductCreate, ProductResponseList, ProductUpdate
from ..auth.dependencies import get_current_admin

router = APIRouter(
    prefix="/product", tags=["Products"], dependencies=[Depends(get_current_admin)]
)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create(product: ProductCreate, service: ProductServiceDep):
    return await service.create(product)


@router.get("/", response_model=ProductResponseList)
async def find_all(query: ProductQueryDep, service: ProductServiceDep):
    return await service.find_all(query)


@router.get("/{product_id}", response_model=ProductResponse)
async def find_by_id(product_id: uuid.UUID, service: ProductServiceDep):
    return await service.find_by_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update(
    product_id: uuid.UUID, product_data: ProductUpdate, service: ProductServiceDep
):
    return await service.update(product_id=product_id, product_data=product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(product_id: uuid.UUID, service: ProductServiceDep):
    return await service.delete(product_id)
