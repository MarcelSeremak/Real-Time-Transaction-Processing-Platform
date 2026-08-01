from dotenv import load_dotenv
from sqlalchemy import create_engine
from utils.logger import get_logger
import pathlib
import os

logger = get_logger("DB_CONNECTION")

dotenv_path = pathlib.Path(__file__).parent.parent.parent / 'config/.env'
load_dotenv(dotenv_path)

def create_url():
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('POSTGRES_DB')

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def get_engine():
    url = create_url()
    engine = create_engine(url)
    try:
        connection = engine.connect()
        logger.info("Connection to the database was successful.")
        connection.close()
    except Exception as e:
        logger.error(f"An error occurred while connecting to the database: {e}")
    return engine