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
    version="0.0.2",
    contact={
        "name": "Цифровая кафедра МФТИ\nСтудент: Логинов Артём Александрович\nГруппа: М07-404",
        "url": "https://github.com/helloginov/fastapi-taskman",
        "email": "loginov.artem@phystech.edu",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.include_router(task.router)
app.include_router(utils.router)
app.include_router(auth.router)
