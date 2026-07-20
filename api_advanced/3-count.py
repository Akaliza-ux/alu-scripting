#!/usr/bin/python3
"""Recursively count given words in a subreddit's hot-post titles."""
import requests


def _count_tokens(tokens, keywords, counts, index=0):
    """Recursively count matching tokens from one title."""
    if index == len(tokens):
        return counts

    word = tokens[index]

    if word in keywords:
        counts[word] = counts.get(word, 0) + keywords.count(word)

    return _count_tokens(tokens, keywords, counts, index + 1)


def _count_titles(titles, keywords, counts=None, index=0):
    """Recursively count words in every title."""
    if counts is None:
        counts = {}

    if index == len(titles):
        return counts

    counts = _count_tokens(
        titles[index].lower().split(),
        keywords,
        counts
    )
    return _count_titles(titles, keywords, counts, index + 1)


def _print_counts(items, index=0):
    """Recursively print sorted word counts."""
    if index == len(items):
        return

    print("{}: {}".format(items[index][0], items[index][1]))
    return _print_counts(items, index + 1)


def count_words(subreddit, word_list, after=None, hot_list=None):
    """Print keyword counts from all hot posts in subreddit."""
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    if after is not None:
        url += "?after={}".format(after)

    headers = {"User-Agent": "alu-word-count/1.0 by u/Akaliza-ux"}
    response = requests.get(
        url,
        headers=headers,
        allow_redirects=False
    )

    if response.status_code != 200:
        return

    data = response.json()["data"]
    hot_list += list(map(
        lambda post: post["data"]["title"],
        data["children"]
    ))

    if data["after"] is not None:
        return count_words(
            subreddit,
            word_list,
            data["after"],
            hot_list
        )

    keywords = list(map(str.lower, word_list))
    counts = _count_titles(hot_list, keywords)

    items = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )
    _print_counts(items)
