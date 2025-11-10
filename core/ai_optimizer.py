import time
import json
from hardware_interface.traffic_light_driver import TrafficLightDriver
from hardware_interface.sensor_interface import SensorInterface

# Подключение функции обновления веб-интерфейса
try:
    from ui.web_server import update_data
except ImportError:
    update_data = None  # если веб-сервер не запущен

class AIOptimizer:
    def __init__(self, mode='simulator'):
        """
        Инициализация оптимизатора.
        mode: 'simulator' или 'hardware'
        """
        self.mode = mode
        self.controller = TrafficLightDriver(simulation=(mode=='simulator'))
        self.sensors = SensorInterface(simulation=(mode=='simulator'))

        # Текущее состояние светофора
        self.current_state = "RED"
        self.state_order = ["RED", "GREEN", "YELLOW"]

        # MQTT
        try:
            from communication.mqtt_client import MQTTClient
            self.network = MQTTClient(client_id="AIOptimizer")
            print("[СЕТЬ] MQTT-клиент успешно инициализирован.")
        except Exception as e:
            print(f"[ОШИБКА СЕТИ] MQTT не инициализирован: {e}")
            self.network = None

        print(f"[ИНФО] Запущен оптимизатор в режиме: {self.mode}")

    def run_cycle(self):
        sensors = self.sensors.get_sensor_data()
        vehicles = sensors["vehicles"]
        pedestrian = sensors["pedestrian"]

        # Цикличное переключение светофора
        next_index = (self.state_order.index(self.current_state) + 1) % len(self.state_order)
        next_state = self.state_order[next_index]

        # Простейшая адаптация по сенсорам
        if self.current_state == "GREEN" and vehicles < 2:
            next_state = "YELLOW"
        elif self.current_state == "RED" and pedestrian:
            next_state = "GREEN"

        self.controller.set_light_state(next_state)
        self.current_state = next_state

        # MQTT публикация
        if self.network:
            msg = json.dumps({
                "vehicles": vehicles,
                "pedestrian": pedestrian,
                "light_state": next_state
            })
            self.network.publish("rakhsh/traffic/state", msg)
            print(f"[MQTT] Опубликовано: {msg}")

        # Обновление веб-дэшборда
        if update_data:
            update_data({
                "vehicles": vehicles,
                "pedestrian": pedestrian,
                "light_state": next_state
            })

        print(f"[ДАННЫЕ] Сенсоры: {sensors} | Светофор: {next_state}")

    def start(self):
        print("[СИСТЕМА] Запуск цикла управления...")
        while True:
            self.run_cycle()
            time.sleep(3)

if __name__ == "__main__":
    optimizer = AIOptimizer(mode='simulator')
    optimizer.start()
