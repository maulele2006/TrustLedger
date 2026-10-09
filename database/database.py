
import os
import sqlite3

if os.environ.get("VERCEL"):
    DATABASE = "/tmp/trustledger.db"
else:
    DATABASE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "trustledger.db",
    )


def get_connection():
    return sqlite3.connect(DATABASE, timeout=10)


def create_table():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                fraud_probability REAL NOT NULL,
                trust_score REAL NOT NULL,
                risk_level TEXT NOT NULL
            )
            """
        )


def save_transaction(
    amount,
    fraud_probability,
    trust_score,
    risk_level,
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO transactions (
                amount,
                fraud_probability,
                trust_score,
                risk_level
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                float(amount),
                float(fraud_probability),
                float(trust_score),
                str(risk_level),
            ),
        )


def get_transactions():
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                id,
                amount,
                fraud_probability,
                trust_score,
                risk_level
            FROM transactions
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()
