from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db, connect_db
from backend.analytics import get_stats

app = FastAPI(title="InnerEdge API")

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
    return {"message": "InnerEdge API Running"}

# ---------------- STATUS ----------------
@app.get("/status")
def status():
    return {
        "system": "InnerEdge",
        "status": "running"
    }

# ---------------- ACCOUNT ----------------
@app.get("/account")
def account(account_id: int = 1):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT balance, equity, free_margin
        FROM accounts
        WHERE id = ?
    """, (account_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "balance": 0,
            "equity": 0,
            "free_margin": 0
        }

    return {
        "balance": row[0],
        "equity": row[1],
        "free_margin": row[2]
    }

# ---------------- ANALYTICS ----------------
@app.get("/analytics")
def analytics(account_id: int = 1):
    return get_stats(account_id)

# ---------------- LEADERBOARD ----------------
@app.get("/leaderboard")
def leaderboard():

    accounts = [
        {"id": 1, "name": "Main"},
        {"id": 2, "name": "Demo"},
        {"id": 3, "name": "Prop Firm A"}
    ]

    results = []

    for acc in accounts:

        stats = get_stats(acc["id"])

        results.append({
            "account_id": acc["id"],
            "name": acc["name"],
            "profit": stats["total_profit"],
            "trades": stats["total_trades"],
            "status": "ACTIVE"
        })

    results.sort(key=lambda x: x["profit"], reverse=True)

    return {"leaderboard": results}