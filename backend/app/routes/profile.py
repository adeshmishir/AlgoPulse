from fastapi import APIRouter, HTTPException
from app.services.leetcode_service import get_user_profile

router = APIRouter()

@router.get("/profile/{username}")
def profile(username: str):
    data = get_user_profile(username)

    if data is None:
        raise HTTPException(status_code=404, detail="LeetCode user not found")

    return {
        "username": data["username"],
        "real_name": data["profile"]["realName"],
        "ranking": data["profile"]["ranking"],
        "reputation": data["profile"]["reputation"],
        "avatar": data["profile"]["userAvatar"],
        "solved": data["submitStats"]["acSubmissionNum"]
    }