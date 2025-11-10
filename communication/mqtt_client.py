import paho.mqtt.client as mqtt
from communication.comm_utils import safe_print

class MQTTClient:
    def __init__(self, client_id="client1", broker="localhost", port=1883):
        self.client = mqtt.Client(client_id=client_id)
        self.broker = broker
        self.port = port
        try:
            self.client.connect(broker, port, 60)
            safe_print(f"[СЕТЬ] Подключено к MQTT-брокеру {broker}:{port}")
        except Exception as e:
            safe_print(f"[СЕТЬ] Ошибка подключения: {e}")

    def publish(self, topic, message):
        try:
            self.client.publish(topic, message)
            safe_print(f"[MQTT] Опубликовано в {topic}: {message}")
        except Exception as e:
            safe_print(f"[MQTT] Ошибка публикации: {e}")
