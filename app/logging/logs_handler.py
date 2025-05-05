
"""Module for handling productivity logs."""

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import ProductivityLog


async def get_or_create_log(session: AsyncSession, user_id: int) -> ProductivityLog:
    """
    Get or create a productivity log for a user.

    Args:
        session (AsyncSession): The database session.
        user_id (int): The ID of the user.

    Returns:
        ProductivityLog: The productivity log for the user.
    """
    result = await session.execute(
        select(ProductivityLog).where(ProductivityLog.user_id == user_id)
    )
    log = result.scalars().first()
    if not log:
        new_log = ProductivityLog(user_id=user_id)
        session.add(new_log)
        await session.commit()
        return new_log
    return log


async def calculate_focus_score(log: ProductivityLog) -> float:
    """
    Calculate the focus score based on simple rules.

    Args:
        log (ProductivityLog): The productivity log.

    Returns:
        float: The calculated focus score.
    """
    base_score = log.tasks_completed * 0.5
    time_factor = 1.2 if datetime.now().hour in [10, 14, 16] else 0.8  # Biological clock
    return min(base_score * time_factor, 100.0)