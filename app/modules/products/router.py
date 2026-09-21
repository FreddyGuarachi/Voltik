import uuid
from fastapi import APIRouter, status, Depends

from .dependencies import ProductServiceDep, ProductQueryDep
from .schemas import (
    ProductResponse,
    ProductCreate,
    ProductResponseList,
    ProductUpdate,
    ProductStockRow,
)
from ..auth.dependencies import CurrentAdminDep, CurrentUserDep

router = APIRouter(prefix="/product", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create(
    product_in: ProductCreate, service: ProductServiceDep, current_user: CurrentAdminDep
):
    return await service.create(product_in)


@router.get("/", response_model=ProductResponseList)
async def find_all(
    query: ProductQueryDep, service: ProductServiceDep, current_user: CurrentAdminDep
):
    return await service.find_all(query)


@router.get("/export", response_model=list[ProductStockRow])
async def export_stock(service: ProductServiceDep, current_user: CurrentUserDep):
    return await service.export_stock()


@router.get("/{product_id}", response_model=ProductResponse)
async def find_by_id(
    product_id: uuid.UUID, service: ProductServiceDep, current_user: CurrentAdminDep
):
    return await service.find_by_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update(
    product_id: uuid.UUID,
    product_data: ProductUpdate,
    service: ProductServiceDep,
    current_user: CurrentAdminDep,
):
    return await service.update(product_id=product_id, product_data=product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    product_id: uuid.UUID, service: ProductServiceDep, current_user: CurrentAdminDep
):
    return await service.delete(product_id)
