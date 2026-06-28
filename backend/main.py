from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db, get_account, get_trades
from backend.analytics import get_stats

app = FastAPI(title="InnerEdge API", version="2.0")

# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- STARTUP ----------------

@app.on_event("startup")
def startup():
    init_db()

# ---------------- ROOT ----------------

@app.get("/")
def home():
    return {
        "system": "InnerEdge",
        "version": "2.0",
        "status": "running"
    }

# ---------------- STATUS ----------------

@app.get("/status")
def status():
    return {
        "status": "ONLINE",
        "database": "CONNECTED"
    }

# ---------------- ACCOUNT ----------------

@app.get("/account")
def account(account_id: int = 1):

    row = get_account(account_id)

    if row is None:
        return {
            "balance": 0,
            "equity": 0,
            "free_margin": 0
        }

    return {
        "id": row["id"],
        "name": row["name"],
        "balance": row["balance"],
        "equity": row["equity"],
        "free_margin": row["free_margin"]
    }

# ---------------- ANALYTICS ----------------

@app.get("/analytics")
def analytics(account_id: int = 1):
    return get_stats(account_id)

# ---------------- TRADES ----------------

@app.get("/trades")
def trades(account_id: int = 1):

    rows = get_trades(account_id)

    return {
        "count": len(rows),
        "trades": [dict(r) for r in rows]
    }

# ---------------- EDGE ----------------

@app.get("/edge")
def edge(account_id: int = 1):

    stats = get_stats(account_id)

    risk_health = max(0, 100 - stats["drawdown"] / 10)

    return {
        "edge_score": stats["quality_score"],
        "performance_grade": stats["grade"],
        "risk_health": round(risk_health, 2),
        "drawdown": stats["drawdown"],
        "challenge_status": "PASSING" if risk_health >= 80 else "WARNING"
    }

# ---------------- LEADERBOARD ----------------

@app.get("/leaderboard")
def leaderboard():

    board = []

    for account_id, name in [
        (1, "Main"),
        (2, "Demo"),
        (3, "Prop Firm")
    ]:
        stats = get_stats(account_id)

        board.append({
            "account_id": account_id,
            "name": name,
            "profit": stats["total_profit"],
            "grade": stats["grade"],
            "edge_score": stats["quality_score"]
        })

    board.sort(key=lambda x: x["profit"], reverse=True)

    return {"leaderboard": board}