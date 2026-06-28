from backend.database import connect_db


def get_trades():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT symbol, volume, profit, time
        FROM trades
        ORDER BY time DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "symbol": r[0],
            "volume": r[1],
            "profit": r[2],
            "time": r[3],
        }
        for r in rows
    ]