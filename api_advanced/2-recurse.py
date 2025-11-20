#!/usr/bin/python3
"""
Recursive function to query the Reddit API and return a list
containing the titles of all hot articles for a given subreddit.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Returns a list of titles of all hot articles for a given subreddit.
    Returns None if the subreddit is invalid.
    """
    if subreddit is None or not isinstance(subreddit, str):
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    headers = {
        "User-Agent": "linux:0-subs:v1.0 (by /u/kellen-mutoni)"
    }

    params = {}
    if after:
        params['after'] = after

    response = requests.get(url,
                            headers=headers,
                            params=params,
                            allow_redirects=False)

    if response.status_code != 200:
        return None

    try:
        data = response.json().get("data")
        new_after = data.get("after")
        children = data.get("children")

        if children:
            for post in children:
                hot_list.append(post.get("data").get("title"))

        if new_after:
            return recurse(subreddit, hot_list, new_after)

        return hot_list

    except Exception:
        return None
