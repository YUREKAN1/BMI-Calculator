
import sqlite3
from pathlib import Path
from datetime import datetime


class DatabaseManager:

    def __init__(self, db_path=None):
        """Initialize the SQLite database."""

        if db_path is None:
            db_path = Path(__file__).resolve().parent / "bmi_records.db"

        self.db_path = str(db_path)

        self.create_tables()

    def get_connection(self):
        """Create a database connection."""

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    def create_tables(self):
        """Create users and BMI records tables."""

        try:
            with self.get_connection() as connection:

                connection.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL COLLATE NOCASE UNIQUE,
                        created_at TEXT NOT NULL
                    )
                """)

                connection.execute("""
                    CREATE TABLE IF NOT EXISTS bmi_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        weight REAL NOT NULL CHECK(weight > 0),
                        height REAL NOT NULL CHECK(height > 0),
                        bmi REAL NOT NULL CHECK(bmi > 0),
                        recorded_at TEXT NOT NULL,

                        FOREIGN KEY (user_id)
                        REFERENCES users(id)
                        ON DELETE CASCADE
                    )
                """)

        except sqlite3.Error as error:
            raise RuntimeError(
                f"Database initialization failed: {error}"
            ) from error

    def add_user(self, name):
        """Create a new user profile and return its ID."""

        name = name.strip() if isinstance(name, str) else ""

        if not name:
            raise ValueError("User name cannot be empty.")

        try:
            with self.get_connection() as connection:

                cursor = connection.execute("""
                    INSERT INTO users (name, created_at)
                    VALUES (?, ?)
                """, (
                    name,
                    datetime.now().isoformat(timespec="seconds")
                ))

                return cursor.lastrowid

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "A user with this name already exists."
            ) from error

    def get_users(self):
        """Retrieve all registered users."""

        try:
            with self.get_connection() as connection:

                rows = connection.execute("""
                    SELECT id, name, created_at
                    FROM users
                    ORDER BY name COLLATE NOCASE
                """).fetchall()

                return [dict(row) for row in rows]

        except sqlite3.Error as error:
            raise RuntimeError(
                f"Could not retrieve users: {error}"
            ) from error

    def get_user(self, user_id):
        """Retrieve a user by ID."""

        try:
            with self.get_connection() as connection:

                row = connection.execute("""
                    SELECT id, name, created_at
                    FROM users
                    WHERE id = ?
                """, (user_id,)).fetchone()

                return dict(row) if row else None

        except sqlite3.Error as error:
            raise RuntimeError(
                f"Could not retrieve user: {error}"
            ) from error

    def save_bmi_record(self, user_id, weight, height, bmi):
        """Save a BMI measurement for a specific user."""

        if weight <= 0 or height <= 0 or bmi <= 0:
            raise ValueError("BMI record values must be positive.")

        try:
            with self.get_connection() as connection:

                cursor = connection.execute("""
                    INSERT INTO bmi_records (
                        user_id,
                        weight,
                        height,
                        bmi,
                        recorded_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id,
                    weight,
                    height,
                    bmi,
                    datetime.now().isoformat(timespec="seconds")
                ))

                return cursor.lastrowid

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Invalid user ID or BMI record values."
            ) from error

        except sqlite3.Error as error:
            raise RuntimeError(
                f"Could not save BMI record: {error}"
            ) from error

    def get_bmi_history(self, user_id):
        """Retrieve BMI records belonging to one user."""

        try:
            with self.get_connection() as connection:

                rows = connection.execute("""
                    SELECT
                        id,
                        user_id,
                        weight,
                        height,
                        bmi,
                        recorded_at
                    FROM bmi_records
                    WHERE user_id = ?
                    ORDER BY recorded_at ASC, id ASC
                """, (user_id,)).fetchall()

                return [dict(row) for row in rows]

        except sqlite3.Error as error:
            raise RuntimeError(
                f"Could not retrieve BMI history: {error}"
            ) from error
