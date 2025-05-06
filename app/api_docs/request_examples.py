"""Request examples for FastAPI API documentation."""

from datetime import date, timedelta
from fastapi import Body

example_create_project = Body(
    openapi_examples={
        "normal": {
            "summary": "Типовой запрос",
            "description": "Типовой запрос для создания проекта",
            "value": {
                "name": "Презентация",
                "description": (
                    "Подготовить презентацию для доклада на конференцию МФТИ"
                )
            },
        },
        "empty_description": {
            "summary": "Запрос без описания",
            "description": (
                "Запрос для создания проекта без указания описания. "
                "В поле `description` будет автоматически подставлено значение `None`"
            ),
            "value": {
                "name": "Проект без описания",
            },
        },
        "invalid": {
            "summary": "Некорректные данные, возвращается ошибка 422",
            "value": {
                "name": 123,
                "description": 456,
            },
        },
    }
)

example_create_task = Body(
    openapi_examples={
        "normal": {
            "summary": "Типовой запрос",
            "description": "Типовой запрос для создания задачи",
            "value": {
                "description": "Подготовить план",
                "assignee": "Иван Иванов",
                "due_date": (date.today() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "project": 1,
                "complexity": 3,
            },
        },
        "empty_date": {
            "summary": "Запрос без указания срока",
            "description": (
                "Запрос для создания задачи без указания крайнего срока исполнения. "
                "В поле `due_date` будет автоматически подставлен завтрашний день"
            ),
            "value": {
                "description": "Отрепетировать выступление",
                "assignee": "Иван Иванов",
                "project": 1,
                "complexity": 2,
            },
        },
        "empty_project": {
            "summary": "Запрос без указания проекта",
            "description": (
                "Запрос для создания задачи без указания ID проекта. "
                "В поле `project` будет автоматически подставлено значение `None`"
            ),
            "value": {
                "description": "Пообедать",
                "assignee": "Иван Иванов",
                "due_date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "complexity": 1,
            },
        },
        "invalid_data": {
            "summary": "Некорректная дата, возвращается ошибка 422",
            "value": {
                "description": "Подготовить презентацию",
                "assignee": "Василий",
                "due_date": "сегодня",
            },
        },
        "invalid_assignee": {
            "summary": "Некорректный исполнитель, возвращается ошибка 422",
            "description": (
                "Запрос для создания задачи с несуществующим исполнителем."
            ),
            "value": {
                "description": "Подготовить план",
                "assignee": "Иван",
                "due_date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
            },
        },
    }
)
