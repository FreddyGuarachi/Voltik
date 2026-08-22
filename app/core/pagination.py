from typing import Literal
from sqlalchemy import Select, select, func
from sqlalchemy.orm import InstrumentedAttribute

from app.core.dependencies import DBSession


async def count_items(stmt: Select, session: DBSession) -> int:
    """Return the total row count for a given SELECT statement.

    Args:
        stmt (Select): The base query whose matching rows will be counted.
        session (DBSession): Active async database session used to execute the query.

    Returns:
        int: Total number of rows, or 0 if the query returns no result.
    """
    items = select(func.count()).select_from(stmt.subquery())
    return await session.scalar(items) or 0


def apply_order(
    stmt: Select, column: InstrumentedAttribute, order_dir: Literal["asc", "desc"]
) -> Select:
    """Apply ascending or descending order to a query on the given column.

    Args:
        stmt (Select): The query to order.
        column (InstrumentedAttribute): Model column to order by.
        order_dir (Literal["asc", "desc"]): Sort direction.

    Returns:
        Select: The query with ordering applied.
    """
    column = column.desc() if order_dir == "desc" else column.asc()
    return stmt.order_by(column)


def paginate(stmt: Select, skip: int, limit: int) -> Select:
    """Apply offset/limit pagination to a query.

    Args:
        stmt (Select): The query to paginate.
        skip (int): Number of rows to skip.
        limit (int): Maximum number of rows to return.

    Returns:
        Select: The query with pagination applied.
    """
    return stmt.offset(skip).limit(limit)
