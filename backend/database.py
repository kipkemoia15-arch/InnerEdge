import sqlite3
from pathlib import Path

DB_PATH = Path("inneredge_new.db")


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # ----------------------------------------------------
    # ACCOUNTS
    # ----------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL DEFAULT 0,
            equity REAL DEFAULT 0,
            free_margin REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ----------------------------------------------------
    # TRADES
    # ----------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            account_id INTEGER,

            ticket INTEGER,

            symbol TEXT,

            direction TEXT DEFAULT 'BUY',

            volume REAL,

            entry_price REAL DEFAULT 0,

            exit_price REAL DEFAULT 0,

            stop_loss REAL DEFAULT 0,

            take_profit REAL DEFAULT 0,

            profit REAL,

            commission REAL DEFAULT 0,

            swap REAL DEFAULT 0,

            strategy TEXT DEFAULT '',

            session TEXT DEFAULT '',

            notes TEXT DEFAULT '',

            time TEXT,

            FOREIGN KEY(account_id) REFERENCES accounts(id)

        )
    """)

    # ----------------------------------------------------
    # DEFAULT ACCOUNT
    # ----------------------------------------------------
    cursor.execute("SELECT COUNT(*) FROM accounts")

    if cursor.fetchone()[0] == 0:

        cursor.execute("""
            INSERT INTO accounts(
                id,
                name,
                balance,
                equity,
                free_margin
            )
            VALUES(
                1,
                'Main',
                1000,
                1000,
                1000
            )
        """)

    conn.commit()
    conn.close()


# ----------------------------------------------------
# SAVE TRADE
# ----------------------------------------------------
def save_trade(
    account_id,
    ticket,
    symbol,
    volume,
    profit,
    time,
    direction="BUY",
    entry_price=0,
    exit_price=0,
    stop_loss=0,
    take_profit=0,
    commission=0,
    swap=0,
    strategy="",
    session="",
    notes=""
):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trades(

            account_id,
            ticket,
            symbol,
            direction,
            volume,
            entry_price,
            exit_price,
            stop_loss,
            take_profit,
            profit,
            commission,
            swap,
            strategy,
            session,
            notes,
            time

        )

        VALUES(
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
    """, (

        account_id,
        ticket,
        symbol,
        direction,
        volume,
        entry_price,
        exit_price,
        stop_loss,
        take_profit,
        profit,
        commission,
        swap,
        strategy,
        session,
        notes,
        time

    ))

    conn.commit()
    conn.close()


# ----------------------------------------------------
# GET ACCOUNT
# ----------------------------------------------------
def get_account(account_id=1):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM accounts
        WHERE id=?
    """, (account_id,))

    row = cursor.fetchone()

    conn.close()

    return row


# ----------------------------------------------------
# GET TRADES
# ----------------------------------------------------
def get_trades(account_id=1):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM trades
        WHERE account_id=?
        ORDER BY id
    """, (account_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows