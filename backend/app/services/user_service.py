from app.models.user import User
from app.models.profile_history import ProfileHistory


def save_or_update_user(db, profile):
    stats = profile["stats"]

    user = db.query(User).filter(User.username == profile["username"]).first()

    if user is None:
        user = User(username=profile["username"])
        db.add(user)

    user.ranking = profile["ranking"]
    user.total_solved = stats["total_solved"]
    user.easy = stats["easy"]
    user.medium = stats["medium"]
    user.hard = stats["hard"]
    user.acceptance = stats["acceptance_estimate"]

    last_history = (
        db.query(ProfileHistory)
        .filter(ProfileHistory.username == profile["username"])
        .order_by(ProfileHistory.created_at.desc())
        .first()
    )

    should_create_history = (
        last_history is None
        or last_history.total_solved != stats["total_solved"]
        or last_history.ranking != profile["ranking"]
    )

    if should_create_history:
        history = ProfileHistory(
            username=profile["username"],
            ranking=profile["ranking"],
            total_solved=stats["total_solved"],
            easy=stats["easy"],
            medium=stats["medium"],
            hard=stats["hard"],
            acceptance=stats["acceptance_estimate"],
        )

        db.add(history)

    db.commit()
    db.refresh(user)

    return user


def get_user_history(db, username):
    history = (
        db.query(ProfileHistory)
        .filter(ProfileHistory.username == username)
        .order_by(ProfileHistory.created_at.asc())
        .all()
    )

    return history