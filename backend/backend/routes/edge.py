from fastapi import APIRouter

router = APIRouter()

@router.get("/edge")
def get_edge():
    return {
        "edge_score": 0,
        "risk_health": 0,
        "performance_grade": "N/A",
        "challenge_status": "UNKNOWN",
        "daily_loss": 0,
        "max_drawdown": 0,
        "consecutive_losses": 0
    }