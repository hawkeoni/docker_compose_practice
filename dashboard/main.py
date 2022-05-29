import os
from collections import Counter
from textwrap import dedent
from typing import List, Tuple

import psycopg2
import seaborn as sns
import streamlit as st
from sklearn.metrics import confusion_matrix

sns.set()


@st.experimental_singleton
def get_connection():
    return psycopg2.connect(
        host="database",
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


@st.cache(ttl=60)
def plot_confusion_matrix() -> List[Tuple[int, int]]:
    conn = get_connection()
    cursor = conn.cursor()
    query = dedent(
        """
    select predicted_class, true_label
    from twitter_data
    where true_label is not NULL
    """
    )
    cursor.execute(query)
    # Here it is obvious that fetchall is expensive, so we'll have to cache it
    # and recalculate only fresh stuff, where Time >= X
    res = cursor.fetchall()
    if res:
        y_pred, y_true = zip(*res)
    else:
        return
    cursor.close()
    matrix = confusion_matrix(y_true, y_pred)
    ax = sns.heatmap(matrix, cmap="magma", annot=True)
    ax.set_title("Confusion Matrix of labeled tweets")
    st.pyplot(ax.figure, clear_figure=True)


@st.cache(ttl=60)
def plot_tweet_activity():
    # we can use this to see general user activity
    # we can also query the classes to see,
    # what sort of activity are we having
    conn = get_connection()
    cursor = conn.cursor()
    query = dedent(
        """
    select time
    from twitter_data
    order by time ASC
    """
    )
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    time = [x[0] for x in res]
    counter = Counter(time)
    time = sorted(list(counter.keys()))
    count = [counter[key] for key in time]
    ax = sns.lineplot(time, count)
    ax.set_title("User activity")
    st.pyplot(ax.figure, clear_figure=True)


def main():
    # Ideas for graphs - confusion matrix, percentage of political tweets, activity
    # There are actually a lot of things to monitor:
    # time of model inference and other hardware metrics
    # but this is neither the time nor the moment for this
    plot_confusion_matrix()
    plot_tweet_activity()


if __name__ == "__main__":
    main()
