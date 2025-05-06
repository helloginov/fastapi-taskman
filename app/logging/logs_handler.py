
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
    
    if log.last_activity.month != datetime.now().month:
        log.tasks_completed_month = 0
        log.mean_complexity_month = 0.0
    log.last_activity = datetime.now()

    return log


async def update_mean_complexity(log: ProductivityLog, complexity: int) -> float:
    """
    Calculate the focus score based on simple rules.

    Args:
        log (ProductivityLog): The productivity log.
        complexity (int): The complexity of the task.

    Returns:
        float: The calculated focus score.
    """
    log.tasks_completed += 1
    log.tasks_completed_month += 1
    log.mean_complexity_month = (
        log.mean_complexity_month * (log.tasks_completed_month - 1) + complexity
    ) / log.tasks_completed_month
    return log