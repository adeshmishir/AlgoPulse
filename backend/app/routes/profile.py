from fastapi import APIRouter, HTTPException
from app.services.leetcode_service import get_user_profile
from app.services.analytics_service import build_profile_analytics

router = APIRouter()

@router.get("/profile/{username}")
def profile(username: str):
    data = get_user_profile(username)

    if data is None:
        raise HTTPException(status_code=404, detail="LeetCode user not found")

    return build_profile_analytics(data)