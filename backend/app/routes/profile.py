from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.leetcode_service import get_user_profile, get_contest_info
from app.services.analytics_service import build_profile_analytics
from app.services.user_service import (
    save_or_update_user,
    get_user_history,
    get_user_summary,
    get_user_growth,
)

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
        raise HTTPException(
            status_code=404,
            detail="User summary not found. Fetch profile first.",
        )

    return summary


@router.get("/profile/{username}/growth")
def profile_growth(username: str, db: Session = Depends(get_db)):
    growth = get_user_growth(db, username)

    if growth is None:
        raise HTTPException(
            status_code=404,
            detail="Not enough history data for growth analysis",
        )

    return growth


@router.get("/profile/{username}/contest")
def profile_contest(username: str):
    contest = get_contest_info(username)

    if contest is None:
        raise HTTPException(
            status_code=404,
            detail="Contest data not found for this user",
        )

    return {
        "username": username,
        "attended_contests": contest["attendedContestsCount"],
        "rating": round(contest["rating"], 2),
        "global_ranking": contest["globalRanking"],
        "total_participants": contest["totalParticipants"],
        "top_percentage": contest["topPercentage"],
    }


@router.get("/profile/{username}/dashboard")
def profile_dashboard(username: str, db: Session = Depends(get_db)):
    profile_data = profile(username, db)
    history_data = profile_history(username, db)

    try:
        summary_data = profile_summary(username, db)
    except HTTPException:
        summary_data = None

    try:
        growth_data = profile_growth(username, db)
    except HTTPException:
        growth_data = None

    try:
        contest_data = profile_contest(username)
    except HTTPException:
        contest_data = None

    return {
        "username": username,
        "profile": profile_data,
        "summary": summary_data,
        "growth": growth_data,
        "contest": contest_data,
        "history": history_data,
    }


@router.get("/compare/{user1}/{user2}")
def compare_users(user1: str, user2: str, db: Session = Depends(get_db)):

    data1 = get_user_profile(user1)
    data2 = get_user_profile(user2)

    if data1 is None:
        raise HTTPException(status_code=404, detail=f"{user1} not found")

    if data2 is None:
        raise HTTPException(status_code=404, detail=f"{user2} not found")

    p1 = build_profile_analytics(data1)
    p2 = build_profile_analytics(data2)

    contest1 = get_contest_info(user1)
    contest2 = get_contest_info(user2)

    winner = {
        "ranking": user1 if p1["ranking"] < p2["ranking"] else user2,
        "solved": user1
        if p1["stats"]["total_solved"] > p2["stats"]["total_solved"]
        else user2,
        "acceptance": user1
        if p1["stats"]["acceptance_estimate"]
        > p2["stats"]["acceptance_estimate"]
        else user2,
    }

    if contest1 and contest2:
        winner["contest_rating"] = (
            user1
            if contest1["rating"] > contest2["rating"]
            else user2
        )

    return {
        "user1": {
            "username": user1,
            "ranking": p1["ranking"],
            "total_solved": p1["stats"]["total_solved"],
            "acceptance": p1["stats"]["acceptance_estimate"],
            "contest_rating": round(contest1["rating"], 2)
            if contest1
            else None,
        },
        "user2": {
            "username": user2,
            "ranking": p2["ranking"],
            "total_solved": p2["stats"]["total_solved"],
            "acceptance": p2["stats"]["acceptance_estimate"],
            "contest_rating": round(contest2["rating"], 2)
            if contest2
            else None,
        },
        "winner": winner,
    }