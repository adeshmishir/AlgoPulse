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