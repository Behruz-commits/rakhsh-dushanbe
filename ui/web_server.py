import os
import threading
from flask import Flask, render_template, jsonify
from communication.mqtt_client import MQTTClient  # ваш MQTT модуль

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

traffic_data = {"vehicles": 0, "pedestrian": False, "light_state": "RED"}

@app.route('/')
def index():
    return render_template('index.html', data=traffic_data)

@app.route('/api/state')
def api_state():
    return jsonify(traffic_data)

def update_data(new_data):
    global traffic_data
    traffic_data = new_data

# ======================
# MQTT подписка
# ======================
def mqtt_thread():
    def on_message(topic, payload):
        import json
        try:
            data = json.loads(payload)
            update_data(data)
            # печать для проверки
            print(f"[MQTT] Данные обновлены: {data}")
        except Exception as e:
            print(f"[MQTT] Ошибка разбора сообщения: {e}")

    client = MQTTClient(client_id="WebServer")
    client.subscribe("rakhsh/traffic/state", callback=on_message)
    client.loop_forever()

# Запуск MQTT в отдельном потоке
threading.Thread(target=mqtt_thread, daemon=True).start()

if __name__ == "__main__":
    print("[ИНФО] Запуск веб-сервера http://127.0.0.1:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)
