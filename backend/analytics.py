from backend.database import get_trades


def calculate_drawdown(equity_curve):
    if not equity_curve:
        return 0

    peak = equity_curve[0]
    max_drawdown = 0

    for value in equity_curve:
        if value > peak:
            peak = value

        drawdown = peak - value

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return round(max_drawdown, 2)


def calculate_grade(score):

    if score >= 95:
        return "S+"

    if score >= 90:
        return "S"

    if score >= 80:
        return "A"

    if score >= 70:
        return "B"

    if score >= 60:
        return "C"

    if score >= 40:
        return "D"

    return "F"


def get_stats(account_id=1):

    trades = get_trades(account_id)

    profits = [float(t["profit"]) for t in trades]

    total_trades = len(profits)

    total_profit = round(sum(profits), 2)

    wins = [p for p in profits if p > 0]

    losses = [p for p in profits if p <= 0]

    win_rate = round(
        (len(wins) / total_trades) * 100,
        2
    ) if total_trades else 0

    gross_profit = sum(wins)

    gross_loss = abs(sum(losses))

    if gross_loss == 0:
        profit_factor = round(gross_profit, 2)
    else:
        profit_factor = round(
            gross_profit / gross_loss,
            2
        )

    equity_curve = []

    running = 0

    for profit in profits:

        running += profit

        equity_curve.append({
            "equity": round(running, 2),
            "profit": round(profit, 2)
        })

    drawdown = calculate_drawdown(
        [p["equity"] for p in equity_curve]
    )

    avg_trade = round(
        total_profit / total_trades,
        2
    ) if total_trades else 0

    avg_win = round(
        gross_profit / len(wins),
        2
    ) if wins else 0

    avg_loss = round(
        gross_loss / len(losses),
        2
    ) if losses else 0

    consecutive_losses = 0
    max_consecutive_losses = 0

    for p in profits:

        if p <= 0:

            consecutive_losses += 1

            if consecutive_losses > max_consecutive_losses:
                max_consecutive_losses = consecutive_losses

        else:

            consecutive_losses = 0

    score = 0

    if win_rate >= 60:
        score += 20
    elif win_rate >= 50:
        score += 10

    if profit_factor >= 2:
        score += 25
    elif profit_factor >= 1.5:
        score += 20
    elif profit_factor >= 1:
        score += 10

    if avg_trade > 0:
        score += 15

    if drawdown < 500:
        score += 15
    elif drawdown < 1000:
        score += 10

    if max_consecutive_losses <= 2:
        score += 10
    elif max_consecutive_losses <= 4:
        score += 5

    consistency = min(15, total_trades)

    score += consistency

    grade = calculate_grade(score)

    return {

        "total_trades": total_trades,

        "total_profit": total_profit,

        "win_rate": win_rate,

        "profit_factor": profit_factor,

        "average_trade": avg_trade,

        "average_win": avg_win,

        "average_loss": avg_loss,

        "drawdown": drawdown,

        "consecutive_losses": max_consecutive_losses,

        "quality_score": score,

        "grade": grade,

        "equity_curve": equity_curve

    }