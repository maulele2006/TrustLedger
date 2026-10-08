import sqlite3

DATABASE = "trustledger.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            fraud_probability REAL NOT NULL,
            trust_score REAL NOT NULL,
            risk_level TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_transaction(amount, fraud_probability, trust_score, risk_level):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (amount, fraud_probability, trust_score, risk_level)
        VALUES (?, ?, ?, ?)
    """, (amount, fraud_probability, trust_score, risk_level))

    connection.commit()
    connection.close()


def get_transactions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, amount, fraud_probability, trust_score, risk_level
        FROM transactions
        ORDER BY id DESC
    """)

    transactions = cursor.fetchall()
    connection.close()

    return transactions