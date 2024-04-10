from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/data", methods=["GET"])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)


@app.route("/log/individual", methods=["POST"])
def log_individual():
    json = request.get_json()
    log = json.get("log")

    with open('trajectories/temp.txt', 'a') as file:
        file.write(log + "\n")

    return jsonify({"log": log})


if __name__ == '__main__':
    app.run(debug=True)
