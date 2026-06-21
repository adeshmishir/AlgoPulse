from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.leetcode_service import get_user_profile
from app.services.analytics_service import build_profile_analytics
from app.services.user_service import save_or_update_user

router = APIRouter()

@router.get("/profile/{username}")
def profile(username: str, db: Session = Depends(get_db)):
    data = get_user_profile(username)

    if data is None:
        raise HTTPException(status_code=404, detail="LeetCode user not found")

    analytics = build_profile_analytics(data)

    save_or_update_user(db, analytics)

    return analytics