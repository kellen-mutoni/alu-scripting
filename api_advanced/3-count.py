#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the titles
of all hot articles, and prints a sorted count of given keywords.
"""
import requests
import re


def count_words(subreddit, word_list, hot_list=None, after=None, counts=None):
    """
    Queries the Reddit API, parses the title of all hot articles,
    and prints a sorted count of given keywords.
    """
    if hot_list is None:
        hot_list = []
    if counts is None:
        # Initialize counts dictionary with lowercase keywords
        counts = {word.lower(): 0 for word in word_list}

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
        # Base case for invalid subreddit, print nothing
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

                # Split title into words and count occurrences of keywords
                for word in clean_title.split():
                    if word in counts:
                        counts[word] += 1

        if new_after:
            # Recursive call
            return count_words(subreddit, word_list, hot_list, new_after, counts)

        # Base case: No more pages, proceed to printing

        # 1. Filter out words with zero count
        final_counts = {k: v for k, v in counts.items() if v > 0}

        # 2. Sort by count (descending: -v) then alphabetically (ascending: k)
        sorted_list = sorted(final_counts.items(), key=lambda x: (-x[1], x[0]))

        # 3. Print results
        for k, v in sorted_list:
            print("{}: {}".format(k, v))

    except Exception:
        # Print nothing if API data structure is invalid
        return
