from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import MetaTrader5 as mt5

app = FastAPI(title="InnerEdge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connect_mt5():
    if not mt5.initialize():
        return False
    return True

@app.get("/")
def home():
    return {"status": "InnerEdge API Running"}

@app.get("/account")
def account():
    if not connect_mt5():
        return {"error": "MT5 connection failed"}

    acc = mt5.account_info()

    return {
        "login": acc.login,
        "server": acc.server,
        "balance": acc.balance,
        "equity": acc.equity,
        "margin": acc.margin,
        "free_margin": acc.margin_free
    }

@app.get("/positions")
def positions():
    if not connect_mt5():
        return {"error": "MT5 connection failed"}

    positions = mt5.positions_get()

    if positions is None:
        return []

    return [
        {
            "symbol": p.symbol,
            "volume": p.volume,
            "profit": p.profit
        }
        for p in positions
    ]