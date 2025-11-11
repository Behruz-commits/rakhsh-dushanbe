# path: ui/web_server.py
import os
import threading
from flask import Flask, render_template, jsonify
from communication.comm_utils import log_event
from communication.mqtt_client import MQTTClient  # реализация должна соответствовать INetworkClient

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE, "templates"), static_folder=os.path.join(BASE, "static"))

state = {"vehicles": 0, "pedestrian": False, "light_state": "RED"}

@app.route("/")
def index():
    return render_template("index.html", data=state)

@app.route("/api/state")
def api_state():
    return jsonify(state)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

def update_state(new):
    global state
    state = new

def mqtt_listener():
    def cb(topic, payload):
        import json
        try:
            data = json.loads(payload)
            update_state(data)
            log_event("info", "mqtt", f"received {topic}", payload=data)
        except Exception:
            log_event("error", "mqtt", "failed parse")
    client = MQTTClient(client_id="webserver")
    client.subscribe("rakhsh/traffic/state", cb)
    client.loop_forever()

threading.Thread(target=mqtt_listener, daemon=True).start()
