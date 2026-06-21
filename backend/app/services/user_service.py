from app.models.user import User


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

    db.commit()
    db.refresh(user)

    return user