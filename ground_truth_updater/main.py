import os
from textwrap import dedent
from typing import Optional, Tuple

import psycopg2
import streamlit as st


@st.experimental_singleton
def get_connection():
    return psycopg2.connect(
        host="database",
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


def fetch_text(tweet_id: str) -> Optional[Tuple[str, int]]:
    conn = get_connection()
    if not tweet_id:
        return None
    cursor = conn.cursor()
    query = dedent(
        """
    select text, true_label
    from twitter_data
    where tweet_id = %s
    """
    )
    cursor.execute(query, (tweet_id,))
    text = cursor.fetchone()
    if text is None:
        return None, None
    return text


def update_ground_truth(tweet: str, true_label: int):
    conn = get_connection()
    cursor = conn.cursor()
    query = dedent(
        """
    UPDATE twitter_data
    SET true_label = %s
    where tweet_id = %s
    """
    )
    cursor.execute(query, (true_label, tweet))
    conn.commit()
    cursor.close()


def main():
    tweet_id = st.text_input("Please, write the tweet you want to label")
    if not tweet_id:
        return
    tweet_text, true_label = fetch_text(tweet_id)
    print(tweet_text)
    print(true_label, true_label is None)
    if not tweet_text:
        st.write(f"No tweet found with id: {tweet_id}")
        return
    st.write("Current tweet:")
    st.write(f"{tweet_text}")
    st.write(f"Tweet class: {true_label if true_label is not None else 'None'}")
    class_input = st.text_input(
        "Please, write the tweet class",
    )
    if class_input in ["0", "1"]:
        class_input = int(class_input)
        update_ground_truth(tweet_id, class_input)
        st.write("Thank you for labeling the tweet")
    elif class_input:
        st.write("The class must be either 0 or 1")
    else:
        st.write("Please write down the class: 0 or 1")


if __name__ == "__main__":
    main()
