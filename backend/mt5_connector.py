import MetaTrader5 as mt5
from datetime import datetime, timedelta


def connect():
    """Initialize MT5 connection"""
    if not mt5.initialize():
        raise Exception("MT5 initialization failed")
    return True


def get_account_info():
    """Get live account information"""

    account = mt5.account_info()

    if account is None:
        return None

    return {
        "balance": account.balance,
        "equity": account.equity,
        "profit": account.profit,
        "margin": account.margin,
        "free_margin": account.margin_free,
    }


def get_positions():
    """Get all open positions"""

    positions = mt5.positions_get()

    if positions is None:
        return []

    data = []

    for p in positions:
        data.append({
            "symbol": p.symbol,
            "volume": p.volume,
            "profit": p.profit,
            "type": p.type,
        })

    return data


def get_closed_trades(days=30):
    """
    Fetch unique closed BUY and SELL trades from MT5.
    """

    date_to = datetime.now()
    date_from = date_to - timedelta(days=days)

    deals = mt5.history_deals_get(date_from, date_to)

    if deals is None:
        return []

    trades = []
    seen_tickets = set()

    for deal in deals:

        # Only completed trade exits
        if deal.entry != mt5.DEAL_ENTRY_OUT:
            continue

        # Ignore deposits, withdrawals, swaps, commissions, etc.
        if deal.type not in (
            mt5.DEAL_TYPE_BUY,
            mt5.DEAL_TYPE_SELL,
        ):
            continue

        # Prevent duplicate tickets
        if deal.ticket in seen_tickets:
            continue

        seen_tickets.add(deal.ticket)

        trades.append({
            "ticket": deal.ticket,
            "symbol": deal.symbol,
            "volume": deal.volume,
            "profit": deal.profit,
            "time": datetime.fromtimestamp(
                deal.time
            ).strftime("%Y-%m-%d %H:%M:%S")
        })

    return trades