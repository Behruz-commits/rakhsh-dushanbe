import time
import json
from hardware_interface.traffic_light_driver import TrafficLightDriver
from hardware_interface.sensor_interface import SensorInterface

# Попытка подключения функции обновления веб-интерфейса
try:
    from ui.web_server import update_data
except ImportError:
    update_data = None  # Если веб-сервер не запущен

class AIOptimizer:
    def __init__(self, mode='simulator'):
        """
        Инициализация оптимизатора управления светофорами.
        mode — режим работы: 'simulator' или 'hardware'
        """
        self.mode = mode

        # Настройка контроллера и сенсоров
        self.controller = TrafficLightDriver(simulation=(mode == 'simulator'))
        self.sensors = SensorInterface(simulation=(mode == 'simulator'))

        if mode == 'simulator':
            print("[ИНФО] Запущен оптимизатор в режиме симуляции.")
        else:
            print("[ИНФО] Запущен оптимизатор в режиме реального оборудования.")

        # Подключение коммуникационного канала (MQTT)
        try:
            from communication.mqtt_client import MQTTClient
            self.network = MQTTClient(client_id="AIOptimizer")
            print("[СЕТЬ] MQTT-клиент успешно инициализирован.")
        except Exception as e:
            print(f"[ОШИБКА СЕТИ] Не удалось инициализировать MQTT-клиент: {e}")
            self.network = None

        print("[ГОТОВО] Инициализация завершена.")

    def run_cycle(self):
        """Один цикл работы оптимизатора"""
        sensors = self.sensors.get_sensor_data()
        vehicles = sensors["vehicles"]
        pedestrian = sensors["pedestrian"]

        # Простая логика управления светофором
        if vehicles > 5:
            next_state = "GREEN"
        elif pedestrian:
            next_state = "RED"
        else:
            next_state = "YELLOW"

        self.controller.set_light_state(next_state)

        # Публикация данных через MQTT
        if self.network:
            msg = json.dumps({
                "vehicles": vehicles,
                "pedestrian": pedestrian,
                "light_state": next_state
            })
            self.network.publish("rakhsh/traffic/state", msg)

        # Обновление веб-интерфейса
        if update_data:
            update_data({
                "vehicles": vehicles,
                "pedestrian": pedestrian,
                "light_state": next_state
            })

        print(f"[ДАННЫЕ] Сенсоры: {sensors} | Светофор: {next_state}")

    def start(self):
        """Основной цикл"""
        print("[СИСТЕМА] Запуск цикла управления...")
        while True:
            self.run_cycle()
            time.sleep(3)

if __name__ == "__main__":
    ai = AIOptimizer(mode='simulator')
    ai.start()
