import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into your system

# Use the Neon URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+psycopg2://")

class Database:
    def __init__(self):
        # We'll use a standard connection for now for simplicity
        import psycopg2
        self.conn_str = os.getenv("DATABASE_URL")

    async def init_db(self):
        import psycopg2
        conn = psycopg2.connect(self.conn_str)
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, data JSONB)")
            cur.execute("CREATE TABLE IF NOT EXISTS events (id SERIAL PRIMARY KEY, data JSONB)")
            cur.execute("CREATE TABLE IF NOT EXISTS logs (id SERIAL PRIMARY KEY, data JSONB)")
            conn.commit()
        conn.close()

    async def insert(self, table, data):
        import psycopg2
        import json
        conn = psycopg2.connect(self.conn_str)
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO {table} (data) VALUES (%s)", (json.dumps(data),))
            conn.commit()
        conn.close()
        return {"status": "success"}

db = Database()