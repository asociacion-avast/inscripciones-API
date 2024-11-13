import os
from flask_sqlalchemy import SQLAlchemy

# https://alembic.sqlalchemy.org/en/latest/

db = SQLAlchemy()

def get_connection_string():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'inscripciones')

    return f'postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}'

