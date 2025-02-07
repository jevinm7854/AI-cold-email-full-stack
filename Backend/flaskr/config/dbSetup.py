from flask_mysqldb import MySQL
import chromadb
from .logger import logger

mysql = MySQL()
chroma_client = client = chromadb.PersistentClient(path="./chromaDB")


def init_db(app):
    mysql.init_app(app)
    logger.info("Database initialized successfully")

    with app.app_context():
        create_db(mysql)
        create_users_table(mysql)


def create_db(mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS coldEmail")
        logger.info("Database created successfully")
        cur.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        raise


def create_users_table(mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS coldEmail.users (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                background TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        logger.info("Users table created successfully")
        cur.close()
    except Exception as e:
        print(f"Error creating users table: {e}")
        raise
