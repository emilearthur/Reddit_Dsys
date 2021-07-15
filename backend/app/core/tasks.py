"""Core task: Connect and Disconnect to db when application starts and stops."""
from typing import Callable
from fastapi import FastAPI

from app.db.tasks import connect_to_db, close_db_connection


def create_start_app_handler(app: FastAPI) -> Callable:
    """Connect to redis and db."""

    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """Disconnect to redis and db."""

    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app