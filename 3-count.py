#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the titles
of all hot articles, and prints a sorted count of given keywords.
"""
import re # Standard library first

import requests # Third-party library, separated by a blank line


def count_words(subreddit, word_list, hot_list=None, after=None, counts=None):
    """
    Queries the Reddit API, parses the title of all hot articles,
    and prints a sorted count of given keywords.
    """
    if hot_list is None:
        hot_list = []
    if counts is None:
        counts = {word.lower(): 0 for word in word_list}

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    headers = {
        "User-Agent": ("linux:0-subs:v1.0 "
                       "(by /u/kellen-mutoni)")
    }

    params = {}
    if after:
        params['after'] = after

    response = requests.get(url,
                            headers=headers,
                            params=params,
                            allow_redirects=False)

    if response.status_code != 200:
        return

    try:
        data = response.json().get("data")
        new_after = data.get("after")
        children = data.get("children")

        if children:
            for post in children:
                title = post.get("data").get("title").lower()

                # Clean title: replace non-alphanumeric chars with space
                clean_title = re.sub(r'[^a-z0-9\s_]', ' ', title)

                for word in clean_title.split():
                    if word in counts:
                        counts[word] += 1

        if new_after:
            return count_words(subreddit, word_list, hot_list, new_after, counts)

        # Base case: No more pages, proceed to printing
        final_counts = {k: v for k, v in counts.items() if v > 0}

        # Sort by count (descending) then alphabetically (ascending)
        sorted_list = sorted(final_counts.items(), key=lambda x: (-x[1], x[0]))

        for k, v in sorted_list:
            print("{}: {}".format(k, v))

    except Exception:
        return
