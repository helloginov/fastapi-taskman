from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select
from datetime import datetime

from app.db import get_async_session, get_session
from app.schemas.task import ProductivityLog, Task, User
from ..api_docs import request_examples
from ..auth.auth_handler import get_current_user
from ..logging.logs_handler import update_mean_complexity, get_or_create_log
from ..schemas import task as schema_task

router = APIRouter(prefix="/tasks", tags=["Управление задачами в БД"])


@router.post(
    "/new_project",
    status_code=status.HTTP_201_CREATED,
    response_model=schema_task.ProjectRead,
    summary="Добавить проект",
)
def create_project(
    project: Annotated[
        schema_task.ProjectCreate, request_examples.example_create_project
    ],
    session: Session = Depends(get_session),
):
    """
    Create a new project.
    """
    new_project = schema_task.Project(
        name=project.name,
        description=project.description,
    )
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project


@router.get(
    "/all_projects",
    status_code=status.HTTP_200_OK,
    response_model=List[schema_task.ProjectRead],
    summary="Список всех проектов",
)
def get_all_projects(session: Session = Depends(get_session)):
    """
    Retrieve all projects.
    """
    projects = session.exec(select(schema_task.Project)).all()
    if not projects:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No projects found.",
        )
    return projects


@router.post(
    "/new_task",
    status_code=status.HTTP_201_CREATED,
    response_model=schema_task.TaskRead,
    summary="Добавить задачу",
)
def create_task(
    task: Annotated[
        schema_task.TaskCreate, request_examples.example_create_task
    ],
    session: Session = Depends(get_session),
):
    """
    Create a new task and assign it to a user.
    """
    statement = select(schema_task.User).where(
        schema_task.User.name == task.assignee
    )
    existing_user = session.exec(statement).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{task.assignee} not found",
        )
    new_task = schema_task.Task(
        description=task.description,
        assignee=existing_user.id,
        due_date=task.due_date,
        project=task.project,
        complexity=task.complexity,
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.get(
    "/project/{project_id}/tasks",
    status_code=status.HTTP_200_OK,
    response_model=List[schema_task.TaskRead],
    summary="Получить все задачи, связанные с определенным проектом",
)
def read_tasks_by_project(
    project_id: int, session: Session = Depends(get_session)
):
    """
    Retrieve all tasks associated with a specific project.
    """
    tasks = session.exec(
        select(schema_task.Task).where(
            schema_task.Task.project == project_id
        )
    ).all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"No tasks found for project ID {project_id}.",
        )
    return tasks


@router.get(
    "/no_project",
    status_code=status.HTTP_200_OK,
    response_model=List[schema_task.TaskRead],
    summary="Получить все задачи, которые не связаны с каким-либо проектом",
)
def read_tasks_without_project(session: Session = Depends(get_session)):
    """
    Retrieve all tasks that are not associated with any project.
    """
    tasks = session.exec(
        select(schema_task.Task).where(schema_task.Task.project == None)
    ).all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No tasks found without a project.",
        )
    return tasks


@router.get(
    "/user/{user_id}/tasks",
    status_code=status.HTTP_200_OK,
    response_model=List[schema_task.TaskRead],
    summary="Получить все задачи, связанные с определенным пользователем",
)
def read_tasks_by_user(
    user_id: int, session: Session = Depends(get_session)
):
    """
    Retrieve all tasks assigned to a specific user.
    """
    tasks = session.exec(
        select(schema_task.Task).where(
            schema_task.Task.assignee == user_id
        )
    ).all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"No tasks found for user ID {user_id}.",
        )
    return tasks


@router.patch(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=schema_task.TaskRead,
    summary="Обновить задачу по ID",
)
def update_task_by_id(
    task_id: int,
    data_for_update: dict,
    session: Session = Depends(get_session),
):
    """
    Update a task by its ID.
    """
    statement = select(schema_task.Task).where(
        schema_task.Task.id == task_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found.",
        )

    for key, value in data_for_update.items():
        if hasattr(task, key):
            setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.post(
    "/{task_id}/complete",
    status_code=status.HTTP_200_OK,
    summary="Завершить задачу",
)
async def complete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """
    Mark a task as completed and update productivity logs.
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found.",
        )
    if task.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task {task_id} is already completed.",
        )
    task.is_completed = True

    log = await get_or_create_log(session, current_user.id)
    log = await update_mean_complexity(log, task.complexity)

    await session.commit()

    month = datetime.now().strftime("%B")
    return {
        "message": f"Task {task_id} marked as completed.",
        f"mean_complexity_{month}": round(log.mean_complexity_month, 2),
        f"tasks_completed_{month}": log.tasks_completed_month,
        "tasks_completed": log.tasks_completed,
    }


@router.get(
    "/user/{user_id}/productivity_log",
    status_code=status.HTTP_200_OK,
    response_model=ProductivityLog,
    summary="Получить лог продуктивности пользователя",
)
async def get_productivity_log(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve the productivity log for a specific user.
    """
    log = await session.get(ProductivityLog, user_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Productivity log for user ID {user_id} not found.",
        )

    return log


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Удалить задачу по ID.",
)
def delete_task_by_id(
    task_id: int, session: Session = Depends(get_session)
):
    """
    Delete a task by its ID.
    """
    statement = select(schema_task.Task).where(
        schema_task.Task.id == task_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found.",
        )

    session.delete(task)
    session.commit()
    return {"deleted task": task}
