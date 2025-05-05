from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import text
from sqlmodel import SQLModel, Session, select

from app.db import engine, get_session
from app.schemas.task import User
from ..auth.auth_handler import get_current_user

router = APIRouter(prefix="/utils", tags=["Вспомогательные инструменты"])


@router.get(
    "/test-db",
    status_code=status.HTTP_200_OK,
    summary="Тест подключения к базе данных",
)
def test_database(session: Session = Depends(get_session)):
    """
    Test database connection by executing a simple query.
    """
    result = session.exec(select(text("'Hello world'"))).all()
    return result


@router.get(
    "/create-db-tables",
    status_code=status.HTTP_200_OK,
    summary="Создать таблицы базы данных",
)
def create_database_tables():
    """
    Create all database tables defined in the SQLModel metadata.
    """
    SQLModel.metadata.create_all(engine)
    return {"message": "Tables created"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.get(
    "/test-auth",
    summary="Посмотреть токен",
)
def show_access_token(token: str = Depends(oauth2_scheme)):
    """
    Display the access token for the current user.
    """
    return {"token": token}


@router.get(
    "/me",
    response_model=int,
    summary="Получить ID вошедшего пользователя",
)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Retrieve the ID of the currently logged-in user.
    """
    return current_user.id
