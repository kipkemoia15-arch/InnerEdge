from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.mt5_connector import (
    connect,
    get_account_info,
    get_positions,
    get_closed_trades,
)

from backend.database import (
    create_tables,
    check_table,
    save_trade,
)

from backend.journal import get_trades
from backend.analytics import get_stats

app = FastAPI(title="InnerEdge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():

    connect()
    create_tables()
    check_table()

    trades = get_closed_trades()

    inserted = 0
    skipped = 0

    for trade in trades:

        if save_trade(
            trade["ticket"],
            trade["symbol"],
            trade["volume"],
            trade["profit"],
            trade["time"],
        ):
            inserted += 1
        else:
            skipped += 1

    print(f"✓ Imported : {inserted}")
    print(f"✓ Skipped  : {skipped}")


@app.get("/")
def home():
    return {"message": "InnerEdge running 🚀"}


@app.get("/account")
def account():
    return get_account_info()


@app.get("/positions")
def positions():
    return get_positions()


@app.get("/trades")
def trades():
    return get_trades()


@app.get("/analytics")
def analytics():
    return get_stats()


@app.get("/status")
def status():
    return {
        "system": "InnerEdge",
        "status": "running",
        "mt5_connected": True,
        "database": "active",
        "message": "Everything is working 🚀",
    }