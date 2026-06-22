from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.leetcode_service import get_user_profile
from app.services.analytics_service import build_profile_analytics
from app.services.user_service import save_or_update_user
from app.services.user_service import save_or_update_user, get_user_history, get_user_summary, get_user_growth

router = APIRouter()

@router.get("/profile/{username}")
def profile(username: str, db: Session = Depends(get_db)):
    data = get_user_profile(username)

    if data is None:
        raise HTTPException(status_code=404, detail="LeetCode user not found")

    analytics = build_profile_analytics(data)

    save_or_update_user(db, analytics)

    return analytics

@router.get("/profile/{username}/history")
def profile_history(username: str, db: Session = Depends(get_db)):
    history = get_user_history(db, username)

    return [
        {
            "date": item.created_at,
            "ranking": item.ranking,
            "total_solved": item.total_solved,
            "easy": item.easy,
            "medium": item.medium,
            "hard": item.hard,
            "acceptance": item.acceptance,
        }
        for item in history
    ]

@router.get("/profile/{username}/summary")
def profile_summary(username: str, db: Session = Depends(get_db)):
    summary = get_user_summary(db, username)

    if summary is None:
        raise HTTPException(status_code=404, detail="User summary not found. Fetch profile first.")

    return summary

@router.get("/profile/{username}/growth")
def profile_growth(username: str, db: Session = Depends(get_db)):
    growth = get_user_growth(db, username)

    if growth is None:
        raise HTTPException(status_code=404, detail="Not enough history data for growth analysis")

    return growth