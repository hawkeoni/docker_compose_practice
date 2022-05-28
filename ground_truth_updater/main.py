import os
from textwrap import dedent
from typing import Tuple, Optional

import psycopg2
import streamlit as st


@st.experimental_singleton
def get_connnection():
    return psycopg2.connect(
            host="database",
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"]
        )


@st.cache()
def fetch_text(conn, tweet_id: str) -> Optional[Tuple[str, int]]:
    if not tweet_id:
        return None
    cursor = conn.cursor()
    query = dedent("""
    select text
    from twitter_data, true_label
    where tweet_id = %s
    """)
    cursor.execute(query, (tweet_id))
    text = cursor.fetchone()
    return text


def update_ground_truth(conn, tweet: str, true_label: int):
    cursor = conn.cursor()
    query = dedent("""
    UPDATE twitter_data
    SET true_label = %s
    where tweet_id = %s
    """)
    cursor.execute(query, (true_label, tweet))
    conn.commit()
    cursor.close()


conn = get_connnection()
tweet_id = st.text_input("Please, write the tweet you want to label")
tweet_text, true_label = fetch_text(conn, tweet_id)
st.write(f"Current tweet:\n{tweet_text}\n\nTweet class: {true_label if true_label else 'None'}")
class_input = st.text_input("Please, write the tweet class", )
if tweet_text is None:
    st.write("No tweet provided for markup")
elif class_input in ["0", "1"]:
    class_input = int(class_input)
    update_ground_truth(conn, tweet_id, class_input)
    st.write("Thank you for labeling the tweet")
elif class_input is None:
    st.write("The class must be either 0 or 1")
else:
    st.write("Please write down the class: 0 or 1")



