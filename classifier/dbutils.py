import os
from textwrap import dedent
from typing import Dict, List, Tuple

import psycopg2

__all__ = [
    "get_connection",
    "write_to_db",
    "update_ground_truth",
    "get_metrics",
    "get_activity",
]


def get_connection(host: str, user: str, password: str):
    return psycopg2.connect(host=host, user=user, password=password)


# I can't really remember, why I did it...
_CONNECTION = None


def get_connection_from_env(reset: bool = False):
    global _CONNECTION
    if reset or _CONNECTION is None:
        _CONNECTION = get_connection(
            host="database",
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
        )
    return _CONNECTION


def write_to_db(data: Dict[str, str], prediction: Dict[str, float]):
    conn = get_connection_from_env()
    cursor = conn.cursor()
    # Actually one symbol away from being and SQL injection
    # Also probably can be faster with prepared statements
    query = dedent(
        """
    insert into twitter_data 
    (tweet_id, username, country, text, time, verified, followers, probability, predicted_class) 
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    )
    data_tuple = (
        data["tweet_id"],
        data["username"],
        data["country"],
        data["text"],
        data["time"],
        data["verified"],
        data["followers"],
        prediction["prob"],
        prediction["class"],
    )
    cursor.execute(query, data_tuple)
    conn.commit()
    cursor.close()
