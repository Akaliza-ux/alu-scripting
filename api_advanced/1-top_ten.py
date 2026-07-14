#!/usr/bin/python3
"""Queries the Reddit API"""
import requests


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts"""

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    headers = {
        "User-Agent": "ALU Reddit API project"
    }

    response = requests.get(
        url,
        headers=headers,
        allow_redirects=False
    )

    if response.status_code != 200:
        print("None")
        return

    data = response.json()

    posts = data["data"]["children"]

    for post in posts[:10]:
        print(post["data"]["title"])
