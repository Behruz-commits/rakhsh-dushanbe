import os
from flask import Flask, render_template, jsonify

# Абсолютный путь к каталогу ui/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Указываем Flask, где шаблоны и статика
TEMPLATE_DIR = os.path.join(BASE_DIR, "dashboard", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "dashboard", "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Начальные данные
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

if __name__ == "__main__":
    print("[ИНФО] Запуск веб-сервера по адресу http://127.0.0.1:5000/")
    print(f"[ИНФО] Используется каталог шаблонов: {TEMPLATE_DIR}")
    app.run(host='0.0.0.0', port=5000, debug=True)
