#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the title of all
hot articles, and prints a sorted count of given keywords.
"""
import requests
import sys


def count_words(subreddit, word_list, after=None, counts={}):
    """
    Recursive function that queries the Reddit API, parses the title of all
    hot articles, and prints a sorted count of given keywords.
    """
    if not after:
        # First call: normalize word_list to lowercase
        word_list = [word.lower() for word in word_list]
        counts = {word: 0 for word in word_list}

    if after is None:
        url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    else:
        url = "https://www.reddit.com/r/{}/hot.json?after={}".format(
            subreddit, after)

    headers = {
        "User-Agent": "linux:0x00.api.advanced:v1.0.0 (by /u/custom_user)"
    }
    
    # Don't follow redirects
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return None

    try:
        data = response.json().get("data")
        children = data.get("children")
        after = data.get("after")

        for child in children:
            title = child.get("data").get("title").lower().split()
            for word in word_list:
                counts[word] += title.count(word)

    except Exception:
        return None

    if after is None:
        # End of recursion: print results
        if not counts:
            return
        
        # Filter out words with 0 count
        results = {k: v for k, v in counts.items() if v > 0}
        
        # Sort: Descending by count, then Alphabetical by word
        # We achieve this by sorting items.
        sorted_results = sorted(results.items(), key=lambda x: (-x[1], x[0]))
        
        for word, count in sorted_results:
            print("{}: {}".format(word, count))
    else:
        return count_words(subreddit, word_list, after, counts)
