from argparse import ArgumentParser
from multiprocessing.sharedctypes import Value

from flask import Flask, jsonify, request

from predictor import RandomPredictor


app = Flask(__name__)
predictor = RandomPredictor()


def write_to_db(data):
    pass


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
    app.run()
