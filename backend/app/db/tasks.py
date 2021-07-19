"""Database Connect Tasks."""

from fastapi import FastAPI
from databases import Database
from app.core.config import DATABASE_URL
from datetime import datetime
import os
import logging

# logging.basicConfig(filename='BackendApp.log', encoding='utf-8', level=logging.DEBUG,
#                     format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',)

logging.basicConfig(handlers=[logging.FileHandler(filename="logs/BackendApp_Server.log", 
                                                 encoding='utf-8', mode='a+')],
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)


async def connect_to_db(app: FastAPI) -> None:
    """Connect to postgres db."""
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else DATABASE_URL
    database = Database(DB_URL, min_size=2, max_size=10)
    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logging.warning("--- DB CONNECTION ERROR ---")
        logging.warning(e)
        logging.warning("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    """Close to postgres db."""
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logging.warning("--- DB DISCONNECT ERROR ---")
        logging.warning(e)
        logging.warning("--- DB DISCONNECT ERROR ---")