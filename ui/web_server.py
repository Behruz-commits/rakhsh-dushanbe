# web_server.py
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Хранилище текущих состояний светофоров
traffic_states = {
    "1": {"color": "RED", "cars": 5, "pedestrian": False, "mode": "auto"},
    "2": {"color": "GREEN", "cars": 3, "pedestrian": True, "mode": "manual"}
}

@app.route('/')
def index():
    return render_template('index.html')

# Получить текущее состояние конкретного светофора
@app.route('/api/state/<light_id>')
def get_state(light_id):
    state = traffic_states.get(light_id, {})
    return jsonify(state)

# Установить режим светофора (например, auto/manual)
@app.route('/api/set_mode', methods=['POST'])
def set_mode():
    data = request.json
    light_id = data.get("light_id")
    mode = data.get("mode")
    if light_id in traffic_states:
        traffic_states[light_id]["mode"] = mode
        # Опционально оповещаем фронтенд через SocketIO
        socketio.emit('update_state', {light_id: traffic_states[light_id]})
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

# SocketIO событие от фронтенда (например, запросить обновление)
@socketio.on('request_state')
def handle_request_state(data):
    light_id = data.get("light_id")
    if light_id in traffic_states:
        socketio.emit('update_state', {light_id: traffic_states[light_id]})

if __name__ == '__main__':
    # Запуск сервера с поддержкой динамики
    socketio.run(app, host='127.0.0.1', port=5000)
