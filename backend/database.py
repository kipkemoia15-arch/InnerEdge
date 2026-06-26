import sqlite3

DB_NAME = "inneredge_new.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket INTEGER UNIQUE,
        symbol TEXT NOT NULL,
        volume REAL NOT NULL,
        profit REAL NOT NULL,
        time TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_trade(ticket, symbol, volume, profit, time):
    """
    Save a trade using the MT5 deal ticket as the unique identifier.
    """

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO trades
        (
            ticket,
            symbol,
            volume,
            profit,
            time
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        ticket,
        symbol,
        volume,
        profit,
        time
    ))

    inserted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return inserted


def get_all_trades():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ticket,
            symbol,
            volume,
            profit,
            time
        FROM trades
        ORDER BY time DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "ticket": row[0],
            "symbol": row[1],
            "volume": row[2],
            "profit": row[3],
            "time": row[4]
        }
        for row in rows
    ]


def check_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(trades)")
    print(cursor.fetchall())

    conn.close()