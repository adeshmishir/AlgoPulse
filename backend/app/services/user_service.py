from app.models.user import User
from app.models.profile_history import ProfileHistory


def save_or_update_user(db, analytics):
    try:
        user = db.query(User).filter(User.username == analytics["username"]).first()

        if user:
            user.ranking = analytics["ranking"]
            user.total_solved = analytics["stats"]["total_solved"]
            user.easy = analytics["stats"]["easy"]
            user.medium = analytics["stats"]["medium"]
            user.hard = analytics["stats"]["hard"]
            user.acceptance = analytics["stats"]["acceptance_estimate"]
        else:
            user = User(
                username=analytics["username"],
                ranking=analytics["ranking"],
                total_solved=analytics["stats"]["total_solved"],
                easy=analytics["stats"]["easy"],
                medium=analytics["stats"]["medium"],
                hard=analytics["stats"]["hard"],
                acceptance=analytics["stats"]["acceptance_estimate"],
            )
            db.add(user)

        db.commit()
        db.refresh(user)

    except Exception as e:
        db.rollback()
        print("Database save error:", e)


def get_user_history(db, username):
    history = (
        db.query(ProfileHistory)
        .filter(ProfileHistory.username == username)
        .order_by(ProfileHistory.created_at.asc())
        .all()
    )

    return history


def get_user_summary(db, username):
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        return None

    total = user.total_solved or 0

    easy_percent = 0
    medium_percent = 0
    hard_percent = 0

    if total > 0:
        easy_percent = round((user.easy / total) * 100, 2)
        medium_percent = round((user.medium / total) * 100, 2)
        hard_percent = round((user.hard / total) * 100, 2)

    return {
        "username": user.username,
        "ranking": user.ranking,
        "total_solved": user.total_solved,
        "easy": user.easy,
        "medium": user.medium,
        "hard": user.hard,
        "easy_percent": easy_percent,
        "medium_percent": medium_percent,
        "hard_percent": hard_percent,
        "acceptance": user.acceptance,
    }


def get_user_growth(db, username):
    history = (
        db.query(ProfileHistory)
        .filter(ProfileHistory.username == username)
        .order_by(ProfileHistory.created_at.asc())
        .all()
    )

    if len(history) < 2:
        return None

    first = history[0]
    latest = history[-1]

    solved_growth = latest.total_solved - first.total_solved
    ranking_change = first.ranking - latest.ranking

    return {
        "username": username,
        "first_snapshot": first.created_at,
        "latest_snapshot": latest.created_at,
        "first_solved": first.total_solved,
        "latest_solved": latest.total_solved,
        "solved_growth": solved_growth,
        "first_ranking": first.ranking,
        "latest_ranking": latest.ranking,
        "ranking_change": ranking_change,
    }