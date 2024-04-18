from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv


parent_folder = os.path.join(os.path.dirname(__file__), "../")
load_dotenv(dotenv_path=os.path.join(parent_folder, ".env"))

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)


@app.route("/log", methods=["POST"])
def log_individual():
    json = request.get_json()
    log = json.get("log")

    with open(parent_folder + "trajectories/log.txt", "a") as file:
        file.write(log + "\n")

    return jsonify({"log": log})


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("FLASK_RUN_PORT"))
