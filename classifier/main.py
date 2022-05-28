import os

import psycopg2
from flask import Flask, jsonify, request

from predictor import RandomPredictor


app = Flask(__name__)
predictor = RandomPredictor()
conn = psycopg2.connect(
    host="database",
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"]
)

    # return {
    #     "tweet_id": str(uuid.uuid4()),
    #     "username": username, 
    #     "country": random.choice(countries),
    #     "message": text,
    #     "time": int(time.time()),
    #     "verified": bool(random.randint(0, 1)),
    #     "followers": random.randint(0, 10000),
    #     }
def write_to_db(data, prediction):
    cursor = conn.cursor()
    cursor.execute("insert into twitter_data "
    "(tweet_id, username, country, text, time, verified, followers ) "
    "values (%s, %s, %s, %s, %s, %s, %s)",
    (
        data["tweet_id"], 
        data["username"], 
        data["country"], 
        data["text"],
        data["time"],
        data["verified"],
        data["followers"],
        # prediction["prob"],
        # prediction["class"]
        ))
    conn.commit()
    cursor.close()


@app.route("/inference", methods=["POST"])
@app.errorhandler(ValueError)
def inference():
    data = request.json
    if "text" not in data:
        return "Wrong request", 400
    prediction = predictor.predict(data)
    write_to_db(data, prediction)
    return jsonify(prediction), 200


if __name__ == "__main__":
    # Could have used IPv6
    port = int(os.environ.get("CLASSIFIER_PORT", 5000))
    app.run(host="0.0.0.0", port=port)

