def build_profile_analytics(data):
    stats = data["submitStats"]["acSubmissionNum"]

    solved_map = {}
    submission_map = {}

    for item in stats:
        solved_map[item["difficulty"]] = item["count"]
        submission_map[item["difficulty"]] = item["submissions"]

    total_solved = solved_map.get("All", 0)
    total_submissions = submission_map.get("All", 0)

    acceptance = 0
    if total_submissions > 0:
        acceptance = round((total_solved / total_submissions) * 100, 2)

    return {
        "username": data["username"],
        "real_name": data["profile"]["realName"],
        "ranking": data["profile"]["ranking"],
        "reputation": data["profile"]["reputation"],
        "avatar": data["profile"]["userAvatar"],
        "stats": {
            "total_solved": total_solved,
            "easy": solved_map.get("Easy", 0),
            "medium": solved_map.get("Medium", 0),
            "hard": solved_map.get("Hard", 0),
            "total_submissions": total_submissions,
            "acceptance_estimate": acceptance
        }
    }