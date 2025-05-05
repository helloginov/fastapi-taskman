from datetime import date, timedelta, datetime
from pydantic import (BaseModel, Field, BeforeValidator, EmailStr)
from pydantic_settings import SettingsConfigDict
from typing import Optional, Annotated, TypeAlias
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field as SQLField


# def _empty_str_or_none(value: str | None) -> None:
#     if value is None or value == "":
#         return None
#     raise ValueError("Expected empty value")


# EmptyStrOrNone: TypeAlias = Annotated[None, BeforeValidator(_empty_str_or_none)]

class ProjectCreate(BaseModel):
    name: str = Field(
        description="Название проекта",
        max_length=100
    )
    description: str = Field(
        description="Описание проекта",
        max_length=1000,
        default=""
    )


class TaskCreate(BaseModel):
    description: str = Field(
        description="Описание задачи",
        max_length=300
    )
    assignee: str       # Если пользователя с таким именем не найдётся, функция создания должна выдать ошибку
    due_date: date | None = Field(
        description="Крайний срок исполнения задачи. "
                    "Не допускаются даты, более ранние, "
                    "чем сегодняшняя.",
        gt=date.today() - timedelta(days=1),
        default=None
    )
    project: int | None = Field(
        description="ID проекта, к которому относится задача",
        default=None
    )
    complexity: int = Field(
        description="Сложность задачи от 1 до 5",
        ge=1, le=5,
        default=1
    )


class ProjectRead(ProjectCreate):
    id: int

class TaskRead(TaskCreate):
    id: int
    is_completed: bool = Field(
        description="Статус выполнения задачи",
        default=False
    )


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    email: str = SQLField(nullable=True, unique_items=True)
    password: str | None
    name: str

    model_config = SettingsConfigDict(
        json_schema_extra = {
            "example": {
                "name": "Иван Иванов",
                "email": "user@example.com",
                "password": "qwerty"
            }
        })

class UserCrendentials(BaseModel):
    email: EmailStr
    password: str

    model_config = SettingsConfigDict(
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "querty"
            }
        })

class Project(SQLModel, ProjectRead, table=True):
    id: int = SQLField(nullable=False, primary_key=True)


class Task(SQLModel, TaskRead, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    due_date: date | None = SQLField(
        description="Крайний срок исполнения задачи. "
                    "Не допускаются даты, более ранние, "
                    "чем сегодняшняя.",
        gt=date.today() - timedelta(days=1),
        default=None
    )
    assignee: int = SQLField(foreign_key="user.id")
    project: int = SQLField(default=None, nullable=True, foreign_key="project.id")
    complexity: int = SQLField(default=1)  # Сложность задачи от 1 до 10
    is_completed: bool = SQLField(default=False)


class ProductivityLog(SQLModel, table=True):
    id: int = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(foreign_key="user.id")
    log_date: date = SQLField(default_factory=date.today)
    tasks_completed: int = SQLField(nullable=False, default=0)  # Количество выполненных задач
    focus_score: float = SQLField(default=0.0)  # "AI"-оценка эффективности
    last_activity: datetime = SQLField(default_factory=datetime.now)
