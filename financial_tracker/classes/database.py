import sqlite3
from typing import Dict, Optional, Tuple, List
from .models import User, Transaction

DATABASE_PATH: str = 'financialTracker.db'

SCHEMAS: Dict[str, str] = {
    'USERS': '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE
            );
        ''',
    'TRANSACTIONS': '''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                type TEXT CHECK(type IN ('expense', 'income')) NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        '''
}

class Database:
    def __init__(self, db_path: str = DATABASE_PATH) -> None:
        try:
            self.connection: sqlite3.Connection = sqlite3.connect(db_path)
            self.cursor: sqlite3.Cursor = self.connection.cursor()
            self.initialize_database()
        except sqlite3.Error as e:
            print(f"Database connection failed: {e}")
            raise e

    def initialize_database(self) -> None:
        try:
            for table_schema in SCHEMAS.values():
                self.cursor.execute(table_schema)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Failed to initialize database: {e}")

    def add_user(self, user: User) -> None:
        try:
            self.cursor.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (user.username,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Failed to add user: {e}")

    def add_transaction(self, transaction: Transaction) -> None:
        try:
            self.cursor.execute(
                "INSERT INTO transactions (user_id, amount, category, date, type) VALUES (?, ?, ?, ?, ?)", 
                (transaction.user_id, transaction.amount, transaction.category, transaction.date, transaction.type)
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Failed to add transaction: {e}")

    def get_user_id(self, username: str) -> Optional[int]:
        try:
            self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Failed to retrieve user ID: {e}")
            return None

    def execute(self, query: str, params: Tuple = ()) -> None:
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Failed to execute query: {e}")

    def fetchall(self, query: str, params: Tuple = ()) -> List[Tuple]:
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Failed to fetch data: {e}")
            return []

class ReportGenerator:
    def __init__(self, db: Database) -> None:
        self.db: Database = db

    def total_expenses(self, user_id: int) -> float:
        result = self.db.fetchall("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'expense'", (user_id,))
        return result[0][0] if result and result[0][0] else 0.0

    def total_income(self, user_id: int) -> float:
        result = self.db.fetchall("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'income'", (user_id,))
        return result[0][0] if result and result[0][0] else 0.0

    def spending_by_category(self, user_id: int) -> Dict[str, float]:
        result = self.db.fetchall("SELECT category, SUM(amount) FROM transactions WHERE user_id = ? AND type = 'expense' GROUP BY category", (user_id,))
        return dict(result)

    def transactions_by_category(self, user_id: int) -> Dict[str, int]:
        result = self.db.fetchall("SELECT category, COUNT(*) FROM transactions WHERE user_id = ? GROUP BY category", (user_id,))
        return dict(result)

    def average_transaction_value_by_category(self, user_id) -> Dict[str, float]:
        result = self.db.fetchall("SELECT category, AVG(amount) FROM transactions WHERE user_id = ? GROUP BY category", (user_id,))
        return dict(result)
