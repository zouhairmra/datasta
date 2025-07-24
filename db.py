# db.py
from sqlalchemy import create_engine
import pandas as pd

def get_connection():
    # Replace these values with your real database credentials
    user = "postgres"
    password = "ZZMM2026"
    host = "localhost"
    port = "5432"
    database = "postgres"
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return engine = create_engine(url)
    
def save_score(username, score, difficulty):
    engine = get_connection()
    with engine.begin() as connection:
        connection.execute(
            "INSERT INTO scores (username, score, difficulty) VALUES (%s, %s, %s)",
            (username, score, difficulty)
        )

