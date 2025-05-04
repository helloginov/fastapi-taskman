from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from ..schemas import task as schema_task
from typing import Annotated, List
from ..api_docs import request_examples

router = APIRouter(prefix="/v2/tasks", tags=["Управление задачами в БД"])

@router.post("/new_project", status_code=status.HTTP_201_CREATED, response_model=schema_task.ProjectRead,
             summary='Добавить проект')
def create_project(
    project: Annotated[schema_task.ProjectCreate, request_examples.example_create_project],
    session: Session = Depends(get_session)
):
    """
    Добавить проект.
    """
    new_project = schema_task.Project(
        name=project.name,
        description=project.description
    )
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project


@router.post("/new_task", status_code=status.HTTP_201_CREATED, response_model=schema_task.TaskRead,
             summary = 'Добавить задачу')
def create_task(
    task: Annotated[schema_task.TaskCreate, request_examples.example_create_task],
    session: Session = Depends(get_session)
):
    """
    Добавить задачу.
    """
    statement = select(schema_task.User).where(schema_task.User.name == task.assignee)
    existing_user = session.exec(statement).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{task.assignee} not found"
        )
    new_task = schema_task.Task(
        description=task.description,
        assignee=existing_user.id,
        due_date=task.due_date,
        project=task.project
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task



@router.get("/project/{project_id}/tasks", status_code=status.HTTP_200_OK, response_model=List[schema_task.TaskRead],
            summary='Получить все задачи, связанные с определенным проектом.')
def read_tasks_by_project(project_id: int, session: Session = Depends(get_session)):

    tasks = session.exec(select(schema_task.Task).where(schema_task.Task.project == project_id)).all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"No tasks found for project ID {project_id}."
        )
    return tasks


@router.get("/tasks/no_project", status_code=status.HTTP_200_OK, response_model=List[schema_task.TaskRead],
            description='Получить все задачи, которые не связаны с каким-либо проектом.')
def read_tasks_without_project(session: Session = Depends(get_session)):

    tasks = session.exec(select(schema_task.Task).where(schema_task.Task.project == None)).all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No tasks found without a project."
        )
    return tasks


@router.get("/user/{user_id}/tasks", status_code=status.HTTP_200_OK, response_model=List[schema_task.TaskRead],
            summary='Получить все задачи, связанные с определенным пользователем.')
def read_tasks_by_user(user_id: int, session: Session = Depends(get_session)):

    tasks = session.exec(select(schema_task.Task).where(schema_task.Task.assignee == user_id)).all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"No tasks found for user ID {user_id}."
        )
    return tasks


@router.patch("/{task_id}", status_code=status.HTTP_200_OK, response_model=schema_task.TaskRead,
              description='Обновить задачу по ID.')
def update_task_by_id(task_id: int, data_for_update: dict, session: Session = Depends(get_session)):

    statement = select(schema_task.Task).where(schema_task.Task.id == task_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )

    for key, value in data_for_update.items():
        if hasattr(task, key):
            setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_200_OK, response_model=schema_task.TaskRead,
              description='Удалить задачу по ID.')
def delete_task_by_id(task_id: int, session: Session = Depends(get_session)):

    statement = select(schema_task.Task).where(schema_task.Task.id == task_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )

    session.delete(task)
    session.commit()
    return {'deleted task': task}
