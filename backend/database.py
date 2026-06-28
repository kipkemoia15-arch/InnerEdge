import sqlite3

DB_PATH = "inneredge_new.db"


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():

    conn = connect_db()
    cursor = conn.cursor()

    # ---------------- ACCOUNTS ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name TEXT,
            balance REAL DEFAULT 0,
            equity REAL DEFAULT 0,
            free_margin REAL DEFAULT 0
        )
    """)

    # ---------------- TRADES ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            ticket INTEGER,
            symbol TEXT,
            volume REAL,
            profit REAL,
            time TEXT
        )
    """)

    # ---------------- SEED DEFAULT ACCOUNT ----------------
    cursor.execute("SELECT COUNT(*) FROM accounts")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
            INSERT INTO accounts (id, name, balance, equity, free_margin)
            VALUES (1, 'Main', 1000, 1000, 1000)
        """)

    conn.commit()
    conn.close()


# ---------------- SAVE TRADE ----------------
def save_trade(account_id, ticket, symbol, volume, profit, time):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trades (account_id, ticket, symbol, volume, profit, time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (account_id, ticket, symbol, volume, profit, time))

    conn.commit()
    conn.close()