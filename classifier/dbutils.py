import os

import psycopg2


_CONNECTION = None
def get_connection():
    global _CONNECTION
    if _CONNECTION is None:
        _CONNECTION = psycopg2.connect(
            host="database",
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"]
        )
    return _CONNECTION


def write_to_db(data, prediction):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("insert into twitter_data "
    "(tweet_id, username, country, text, time, verified, followers, probability, predicted_class ) "
    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (
        data["tweet_id"], 
        data["username"], 
        data["country"], 
        data["text"],
        data["time"],
        data["verified"],
        data["followers"],
        prediction["prob"],
        prediction["class"]
        ))
    conn.commit()
    cursor.close()


# import os
# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base


# class DB:

#     def __init__(self):
#         username = os.environ["POSTGRES_USER"]
#         password = os.environ["POSTGRES_PASSWORD"]
#         dbname = os.environ["POSTGRES_DB"]
#         engine = sqlalchemy.create_engine(f"postgresql://{username}:{password}@database:5432/{dbname}")
#         engine.connect()
#         base = automap_base()
#         base.prepare(engine, reflect=True)
#         twitter_data = base.classes.twitter_data
#         self.engine = engine
#         self.table = twitter_data
    
#     def write(self, data, prediction):
#         pass



# def write_to_db(engine, data, prediction):
#     base = automap_base()
#     with engine.connect() as conn:
#         conn.execute()