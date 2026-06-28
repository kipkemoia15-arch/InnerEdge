from backend.database import connect_db


def get_stats():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT profit, time FROM trades ORDER BY time ASC")
    rows = cursor.fetchall()

    total_trades = len(rows)
    total_profit = sum(r[0] for r in rows) if rows else 0

    equity_curve = []
    running = 0

    for r in rows:
        running += r[0]
        equity_curve.append({
            "time": r[1],
            "equity": running
        })

    conn.close()

    return {
        "total_trades": total_trades,
        "total_profit": total_profit,
        "equity_curve": equity_curve
    }