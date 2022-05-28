import os

from flask import Flask, jsonify, request

from predictor import RandomPredictor
from dbutils import write_to_db


app = Flask(__name__)
predictor = RandomPredictor()


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

