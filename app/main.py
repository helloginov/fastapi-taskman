from fastapi import FastAPI
from app.routes import (task, utils, async_routes, auth)
from app.routes import task
# from contextlib import asynccontextmanager  # Uncomment if you need to create tables on app start >>>
# from app.db import init_database

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#    init_database()
#    yield                                   # <<< Uncomment if you need to create tables on app start


app = FastAPI(
    # lifespan=lifespan,  # Uncomment if you need to create tables on app start
    title="Система управления задачами",
    description="Простейшая система управления задачами, основанная на "
                "фреймворке FastAPI.",
    version="0.0.1",
    contact={
        "name": "Цифровая кафедра МФТИ",
        "url": "https://mipt.ru",
        "email": "digitaldepartments@mipt.ru",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# app.include_router(task.router)
app.include_router(task.router)
app.include_router(utils.router)
app.include_router(async_routes.router)
app.include_router(auth.router)
