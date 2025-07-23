# db.py
from sqlalchemy import create_engine
import pandas as pd

def get_connection():
    # Replace with your own credentials
    return create_engine("postgresql://username:password@hostname:port/dbname")

def save_score(username, score, quiz_type):
    engine = get_connection()
    df = pd.DataFrame([{"username": username, "score": score, "quiz_type": quiz_type}])
    df.to_sql("quiz_scores", engine, if_exists="append", index=False)

def load_scores(username=None):
    engine = get_connection()
    query = "SELECT * FROM quiz_scores"
    if username:
        query += f" WHERE username = '{username}'"
    return pd.read_sql(query, engine)

