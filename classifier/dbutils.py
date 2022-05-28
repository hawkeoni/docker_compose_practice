import os
from typing import List, Tuple, Dict
from textwrap import dedent

import psycopg2


__all__ = [
    "get_connection", 
    "write_to_db", 
    "update_ground_truth",
    "get_metrics",
    "get_activity"
]


def get_connection(host: str, user: str, password: str):
    return psycopg2.connect(host=host, user=user, password=password)

_CONNECTION = None
def get_connection_from_env(reset: bool = False):
    global _CONNECTION
    if reset or _CONNECTION is None:
        _CONNECTION = get_connection(
            host="database",
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"]
        )
    return _CONNECTION


def write_to_db(data: Dict[str, str], prediction: Dict[str, float]):
    conn = get_connection_from_env()
    cursor = conn.cursor()
    # Actually one symbol away from being and SQL injection
    # Also probably can be faster with prepared statements
    query = dedent("""
    insert into twitter_data 
    (tweet_id, username, country, text, time, verified, followers, probability, predicted_class) 
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """)
    data_tuple = (
        data["tweet_id"], 
        data["username"], 
        data["country"], 
        data["text"],
        data["time"],
        data["verified"],
        data["followers"],
        prediction["prob"],
        prediction["class"]
        )
    cursor.execute(query, data_tuple)
    conn.commit()
    cursor.close()


def update_ground_truth(tweet: str, true_label: int):
    conn = get_connection_from_env()
    cursor = conn.cursor()
    query = dedent("""
    UPDATE twitter_data
    SET true_label = %s
    where tweet_id = %s
    """)
    cursor.execute(query, (true_label, tweet))
    conn.commit()
    cursor.close()


def get_metrics() -> List[Tuple[int, int]]:
    conn = get_connection_from_env()
    cursor = conn.cursor()
    query = dedent("""
    select predicted_class, true_label
    from twitter_data
    where true_label is not NULL
    """)
    cursor.execute(query)
    # Here it is obvious that fetchall is expensive, so we'll have to cache it
    # and recalculate only fresh stuff, where Time >= X
    res = cursor.fetchall()
    cursor.close()
    return res


def get_activity():
    # we can use this to see general user activity
    conn = get_connection_from_env()
    cursor = conn.cursor()
    query = dedent("""
    select time, predicted_class
    from twitter_data
    """)
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    return res


