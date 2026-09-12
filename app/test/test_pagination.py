from sqlalchemy import select

from app.core.pagination import paginate, apply_order
from app.modules.products.models import Product


def test_paginate():
    stmt = select(Product)

    result = paginate(stmt=stmt, skip=0, limit=3)

    stmt_expected = stmt.offset(0).limit(3)

    assert str(result) == str(stmt_expected)


def test_apply_order():
    stmt = select(Product)
    column = Product.sku
    order_dir = "desc"

    result = apply_order(stmt=stmt, column=column, order_dir=order_dir)

    stmt_expected = stmt.order_by(column.desc())

    assert str(result) == str(stmt_expected)
