import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("DB_HOST")  # Not MYSQL_HOST
    MYSQL_USER = os.getenv("DB_USER")  # Not MYSQL_USER
    MYSQL_PASSWORD = os.getenv("DB_PASS")
