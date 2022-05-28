import os
from textwrap import dedent
from typing import Tuple, Optional

import psycopg2
import streamlit as st


@st.experimental_singleton
def get_connection():
    return psycopg2.connect(
            host="database",
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"]
        )


@st.cache()
def fetch_text(tweet_id: str) -> Optional[Tuple[str, int]]:
    conn = get_connection()
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


def update_ground_truth(tweet: str, true_label: int):
    conn = get_connection()
    cursor = conn.cursor()
    query = dedent("""
    UPDATE twitter_data
    SET true_label = %s
    where tweet_id = %s
    """)
    cursor.execute(query, (true_label, tweet))
    conn.commit()
    cursor.close()


def main():
    conn = get_connnection()
    tweet_id = st.text_input("Please, write the tweet you want to label")
    tweet_text, true_label = fetch_text(tweet_id)
    if tweet_text is None:
        st.write(f"No tweet found with id: {tweet_id}")
        return
    st.write(f"Current tweet:\n{tweet_text}\n\nTweet class: {true_label if true_label else 'None'}")
    class_input = st.text_input("Please, write the tweet class", )
    if class_input in ["0", "1"]:
        class_input = int(class_input)
        update_ground_truth(tweet_id, class_input)
        st.write("Thank you for labeling the tweet")
    elif class_input is None:
        st.write("The class must be either 0 or 1")
    else:
        st.write("Please write down the class: 0 or 1")

if __name__ == "__main__":
    main()

