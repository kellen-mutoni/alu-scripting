#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first 10
hot posts for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.
    If the subreddit is invalid, prints None.
    """
    if subreddit is None or not isinstance(subreddit, str):
        print("None")
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    
    headers = {
        "User-Agent": "linux:0-subs:v1.0 (by /u/kellen-mutoni)"
    }
    
    params = {
        "limit": 10
    }

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code != 200:
        print("None")
        return

    try:
        data = response.json().get("data")
        children = data.get("children")
        
        # This is the logic fix:
        # Check if data or children is missing OR if children is an empty list
        if not data or not children or len(children) == 0:
            print("None")
            return

        for post in children:
            print(post.get("data").get("title"))
    
    except Exception:
        print("None")
