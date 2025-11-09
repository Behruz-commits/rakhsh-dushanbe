# Простая отправка данных на центральный узел
import json

def send_data_to_central(data):
    print("Отправка данных на ЦУАК:", json.dumps(data))

if __name__ == "__main__":
    data = {"intersection": "Crossroad-1", "vehicles": 12, "pedestrians": 5}
    send_data_to_central(data)
