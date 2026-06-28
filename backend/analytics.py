from backend.database import connect_db


def get_stats(account_id=1):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT profit, symbol, volume, time
        FROM trades
        WHERE account_id = ?
    """, (account_id,))

    rows = cursor.fetchall()

    profits = [r[0] for r in rows]

    total_trades = len(profits)
    total_profit = sum(profits) if profits else 0

    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p <= 0]

    win_rate = (len(wins) / total_trades * 100) if total_trades else 0

    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))

    profit_factor = (gross_profit / gross_loss) if gross_loss != 0 else gross_profit

    # EQUITY CURVE
    equity_curve = []
    running = 0

    for p in profits:
        running += p
        equity_curve.append({
            "equity": running,
            "profit": p
        })

    # AI SCORE ENGINE
    avg_trade = total_profit / total_trades if total_trades else 0

    quality_score = 0

    if win_rate > 55:
        quality_score += 30
    elif win_rate > 45:
        quality_score += 15

    if profit_factor > 1.5:
        quality_score += 40
    elif profit_factor > 1:
        quality_score += 20

    if avg_trade > 0:
        quality_score += 30

    if quality_score >= 80:
        grade = "A - STRONG EDGE"
    elif quality_score >= 60:
        grade = "B - GOOD"
    elif quality_score >= 40:
        grade = "C - WEAK"
    else:
        grade = "D - LOSING EDGE"

    conn.close()

    return {
        "total_trades": total_trades,
        "total_profit": round(total_profit, 2),
        "win_rate": round(win_rate, 2),
        "profit_factor": round(profit_factor, 2),
        "avg_trade": round(avg_trade, 2),
        "quality_score": quality_score,
        "grade": grade,
        "equity_curve": equity_curve
    }