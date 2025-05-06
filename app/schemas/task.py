from datetime import date, datetime, timedelta
from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import SettingsConfigDict
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field as SQLField


class ProjectCreate(BaseModel):
    """
    Schema for creating a new project.
    """
    name: str = Field(
        description="Название проекта",
        max_length=100,
    )
    description: str = Field(
        description="Описание проекта",
        max_length=1000,
        default="",
    )


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.
    """
    description: str = Field(
        description="Описание задачи",
        max_length=300,
    )
    assignee: str  # If the user with this name is not found, an error should be raised.
    due_date: Optional[date] = Field(
        description=(
            "Крайний срок исполнения задачи. "
            "Не допускаются даты, более ранние, чем сегодняшняя."
        ),
        gt=date.today() - timedelta(days=1),
        default=None,
    )
    project: Optional[int] = Field(
        description="ID проекта, к которому относится задача",
        default=None,
    )
    complexity: int = Field(
        description="Сложность задачи от 1 до 5",
        ge=1,
        le=5,
        default=1,
    )


class ProjectRead(ProjectCreate):
    """
    Schema for reading project details.
    """
    id: int


class TaskRead(TaskCreate):
    """
    Schema for reading task details.
    """
    id: int


class User(SQLModel, table=True):
    """
    User model for the database.
    """
    __table_args__ = (UniqueConstraint("email"),)
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    email: str = SQLField(nullable=True, unique_items=True)
    password: Optional[str]
    name: str

    model_config = SettingsConfigDict(
        json_schema_extra={
            "example": {
                "name": "Иван Иванов",
                "email": "user@example.com",
                "password": "qwerty",
            }
        }
    )


class UserCrendentials(BaseModel):
    """
    Schema for user credentials.
    """
    email: EmailStr
    password: str

    model_config = SettingsConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "qwerty",
            }
        }
    )


class Project(SQLModel, ProjectRead, table=True):
    """
    Project model for the database.
    """
    id: int = SQLField(nullable=False, primary_key=True)


class Task(SQLModel, TaskRead, table=True):
    """
    Task model for the database.
    """
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    due_date: Optional[date] = SQLField(
        description=(
            "Крайний срок исполнения задачи. "
            "Не допускаются даты, более ранние, чем сегодняшняя."
        ),
        gt=date.today() - timedelta(days=1),
        default=None,
    )
    assignee: int = SQLField(foreign_key="user.id")
    project: Optional[int] = SQLField(
        default=None, nullable=True, foreign_key="project.id"
    )
    is_completed: bool = SQLField(default=False)
    complexity: int = SQLField(
        description="Сложность задачи от 1 до 5",
        ge=1,
        le=5,
        default=1,
    )


class ProductivityLog(SQLModel, table=True):
    """
    Productivity log model for the database.
    """
    id: int = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(foreign_key="user.id")
    log_date: date = SQLField(default_factory=date.today)
    tasks_completed: int = SQLField(
        nullable=False, default=0
    ) 
    tasks_completed_month: int = SQLField(
        nullable=False, default=0
    )  
    mean_complexity_month: float = SQLField(
        nullable=False, default=0.0
    ) 
    last_activity: datetime = SQLField(
        default_factory=lambda: datetime.now()
    )
