import os
import logging

#from databases import Database
from datetime import datetime
from utils.models import Extracted_Created_Date, Subreddit, SubredditDB

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


POSTGRES_USER =os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"
print(db_url)
engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))

def datetimefixer(extracted_at: float, created_at: float) -> Extracted_Created_Date:
    extracted_at = datetime.utcfromtimestamp(extracted_at).utcnow()
    created_at = datetime.utcfromtimestamp(created_at).utcnow()
    return Extracted_Created_Date(extracted_at=extracted_at,created_at=created_at) 




# async def connect_to_db():
#     db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
#     database = Database(db_url)
#     try:
#         await database.connect()
#     except Exception as e:
#         logging.warning("--- DB CONNECTION ERROR ---")
#         logging.warning(e)
#         logging.warning("--- DB CONNECTION ERROR ---")
#     return database

