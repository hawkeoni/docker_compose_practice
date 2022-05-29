import os
import json
import random
import socket
import sys
import time

import streamlit as st


def get_tweets():
    # HOST, PORT = "fake_twitter", int(os.environ.get("FAKE_TWITTER_PORT", 7000))
    HOST, PORT = "localhost", 7000
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


for tweet in get_tweets():
    st.write(tweet)


