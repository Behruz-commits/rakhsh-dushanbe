import time, json
import paho.mqtt.client as mqtt

c = mqtt.Client()
c.connect("localhost",1883,60)
for i in range(1,100):
    payload = {
        "intersection_id":"1",
        "light_state": "GREEN" if i%3==0 else "RED",
        "vehicles": i%12,
        "pedestrian": (i%4==0),
        "optimizer_mode":"auto",
        "optimizer_decision": f"Test step {i}"
    }
    c.publish("rakhsh/traffic/state", json.dumps(payload, ensure_ascii=False))
    print("published", payload)
    time.sleep(1)
