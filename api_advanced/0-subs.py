#!/usr/bin/python3
"""
Queries the Reddit API and returns the number of subscribers
for a given subreddit.
"""
import requests


def number_of_subscribers(subreddit):
    """
    Returns the number of subscribers for a given subreddit.
    Returns 0 if the subreddit is invalid.
    """
    if subreddit is None or not isinstance(subreddit, str):
        return 0

    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)

    # This User-Agent format is what the project expects
    headers = {
        "User-Agent": "linux:0-subs:v1.0 (by /u/kellen-mutoni)"
    }

    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return 0

    try:
        data = response.json().get("data")
        subscribers = data.get("subscribers", 0)
        return subscribers
    except Exception:
        return 0
