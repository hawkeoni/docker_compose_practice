import json
import os
import random
import socket
import sys
import time
from textwrap import dedent
from typing import Any, Dict

import requests
import streamlit as st


def get_tweets():
    HOST, PORT = "fake_twitter", int(os.environ.get("FAKE_TWITTER_PORT", 7000))
    # Adding strings is bad
    cur_buffer = ""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        while True:
            received = str(sock.recv(1024), "utf-8")
            cur_buffer += received
            if "\n" in cur_buffer:
                tweet, cur_buffer = cur_buffer.split("\n", 1)
                tweet = json.loads(tweet)
                yield tweet


def get_prediction(tweet: Dict[str, Any]):
    port = os.environ.get("CLASSIFIER_PORT", 5000)
    resp = requests.post(f"http://classifier:{port}/inference", json=tweet)
    prediction = resp.json()
    return prediction


def draw_tweet(tweet: Dict[str, Any]):
    st.markdown(
        dedent(
            f"""
    
    **Tweet ID**: {tweet["tweet_id"]}

    **Author**: {tweet["username"]} {"Verified" if tweet["verified"] else ""}

    {tweet["text"]}

    **Text class**: {"Politics" if tweet["class"] else "Non-Political"}

    ----
    """
        )
    )


if __name__ == "__main__":
    for tweet in get_tweets():
        prediction = get_prediction(tweet)
        tweet.update(prediction)
        draw_tweet(tweet)
