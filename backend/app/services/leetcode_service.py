import requests

LEETCODE_URL = "https://leetcode.com/graphql"


def get_user_profile(username: str):
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        profile {
          realName
          ranking
          reputation
          userAvatar
        }
        submitStats {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
      }
    }
    """

    payload = {
        "query": query,
        "variables": {"username": username}
    }

    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com"
    }

    response = requests.post(
        LEETCODE_URL,
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("data", {}).get("matchedUser") is None:
        return None

    return data["data"]["matchedUser"]


def get_contest_info(username: str):
    query = """
    query userContestRankingInfo($username: String!) {
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
      }
    }
    """

    payload = {
        "query": query,
        "variables": {"username": username}
    }

    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com"
    }

    response = requests.post(
        LEETCODE_URL,
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        return None

    data = response.json()

    return data["data"]["userContestRanking"]