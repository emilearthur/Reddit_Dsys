"""Core task: Connect and Disconnect to db when application starts and stops."""
from typing import Callable
from fastapi import FastAPI
import logging

from app.db.tasks import connect_to_db, close_db_connection


logging.basicConfig(handlers=[logging.FileHandler(filename="logs/BackendApp_Server.log", 
                                                 encoding='utf-8', mode='a+')],
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)


def create_start_app_handler(app: FastAPI) -> Callable:
    """Connect to db."""
    #logging.INFO("Application starting")
    logging.info('Starting Server')
    async def start_app() -> None:
        logging.info('Connecting to Database')
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """Disconnect and db."""
    logging.info('Shuting down Server')
    async def stop_app() -> None:
        logging.info('Disconnecting from Database')
        await close_db_connection(app)

    return stop_app