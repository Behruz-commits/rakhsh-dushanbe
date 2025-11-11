# path: communication/mqtt_client.py
import paho.mqtt.client as mqtt
from communication.comm_utils import decode_message, log_event

class MQTTClient:
    def __init__(self, client_id="rakhsh", broker="localhost", port=1883, tls=None, username=None, password=None):
        self._client = mqtt.Client(client_id=client_id)
        if username and password:
            self._client.username_pw_set(username, password)
        if tls:
            self._client.tls_set(**tls)  # tls config stub
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._callbacks = {}
        try:
            self._client.connect(broker, port, 60)
        except Exception as e:
            log_event("error", "mqtt", "connect_failed", error=str(e))

    def _on_connect(self, client, userdata, flags, rc):
        log_event("info", "mqtt", f"connected rc={rc}")

    def _on_message(self, client, userdata, msg):
        cb = self._callbacks.get(msg.topic)
        if cb:
            cb(msg.topic, msg.payload.decode())

    def publish(self, topic, payload):
        self._client.publish(topic, payload)

    def subscribe(self, topic, callback):
        self._callbacks[topic] = callback
        self._client.subscribe(topic)

    def loop_forever(self):
        self._client.loop_forever()
