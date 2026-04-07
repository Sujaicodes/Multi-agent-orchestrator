import aiosqlite
import json
from typing import Dict, Any

class Database:
    def __init__(self, db_name="jarvis.db"):
        self.db_name = db_name

    async def init_db(self):
        """Creates the database tables if they don't exist yet."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)")
            await db.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)")
            await db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)")
            await db.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)")
            await db.commit()

    async def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Inserts a JSON record into the specified SQL table."""
        async with aiosqlite.connect(self.db_name) as db:
            # We store the data as a JSON string so it handles flexible AI outputs
            query = f"INSERT INTO {table} (data) VALUES (?)"
            await db.execute(query, (json.dumps(data),))
            await db.commit()
        return {"status": "success", "data": data}

    async def fetch_all(self, table: str) -> list:
        """Retrieves all records from a table."""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(f"SELECT data FROM {table}") as cursor:
                rows = await cursor.fetchall()
                # Convert the JSON strings back into Python dictionaries
                return [json.loads(row[0]) for row in rows]

# Singleton instance
db = Database()