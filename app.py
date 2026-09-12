from flask import Flask, render_template, request, jsonify
import time
import threading

app = Flask(__name__)

state = {
    "running": False,
    "counter": 0,
    "video_url": "",
    "username": ""
}

def simulation_worker():
    while state["running"]:
        time.sleep(5)

        if state["running"]:
            state["counter"] += 1


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()

    state["username"] = data.get("username", "")
    state["video_url"] = data.get("video_url", "")
    state["running"] = True

    thread = threading.Thread(
        target=simulation_worker,
        daemon=True
    )
    thread.start()

    return jsonify({
        "success": True,
        "message": "Simulation started"
    })


@app.route("/stop", methods=["POST"])
def stop():
    state["running"] = False

    return jsonify({
        "success": True
    })


@app.route("/reset", methods=["POST"])
def reset():
    state["running"] = False
    state["counter"] = 0

    return jsonify({
        "success": True
    })


@app.route("/status")
def status():
    return jsonify(state)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )