from app.schemas.task import User, ProductivityLog
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select


async def get_or_create_log(session: AsyncSession, user_id: int) -> ProductivityLog:
    """Получить или создать лог продуктивности для пользователя"""
    log = await session.execute(
        select(ProductivityLog).where(ProductivityLog.user_id == user_id)
    )
    log = log.scalars().first()
    if not log:
        new_log = ProductivityLog(user_id=user_id)
        session.add(new_log)
        await session.commit()
        return new_log
    return log


async def calculate_focus_score(log: ProductivityLog) -> float:
    """'Умный' расчет на основе простых правил"""
    base_score = log.tasks_completed * 0.5
    time_factor = 1.2 if datetime.now().hour in [10, 14, 16] else 0.8  # "Биологические часы"
    return min(base_score * time_factor, 100.0)