import os

from databases import Database
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the env")

database = Database(DATABASE_URL)

#engine = create_engine(DATABASE_URL)
