#!/usr/bin/python3
"""Recursively retrieve all hot-post titles from a subreddit."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return all hot-post titles for subreddit, or None if unavailable."""
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    if after is not None:
        url += "?after={}".format(after)

    headers = {"User-Agent": "alu-recurse/1.0 by u/Akaliza-ux"}
    response = requests.get(
        url,
        headers=headers,
        allow_redirects=False
    )

    if response.status_code != 200:
        return None

    data = response.json()["data"]
    hot_list += [post["data"]["title"] for post in data["children"]]

    if data["after"] is None:
        return hot_list if hot_list else None

    return recurse(subreddit, hot_list, data["after"])
