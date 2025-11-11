# path: core/ai_optimizer.py
import time
import json
import logging
from core.interfaces import ILightDriver, ISensor, INetworkClient

logger = logging.getLogger("rakhsh.ai")

class AIOptimizer:
    def __init__(self, light_driver: ILightDriver, sensor: ISensor, network: INetworkClient=None):
        self.light = light_driver
        self.sensor = sensor
        self.network = network
        self.state_order = ["RED", "GREEN", "YELLOW"]
        self.current = self.light.get_state() if hasattr(self.light, "get_state") else "RED"
        logger.info("AIOptimizer initialized", extra={"mode": "simulator"})

    def run_cycle(self):
        s = self.sensor.read()
        vehicles = s.get("vehicles", 0)
        pedestrian = s.get("pedestrian", False)

        # примитив: крутить по циклу + адаптация
        next_idx = (self.state_order.index(self.current) + 1) % len(self.state_order)
        next_state = self.state_order[next_idx]

        if self.current == "GREEN" and vehicles < 2:
            next_state = "YELLOW"
        if self.current == "RED" and pedestrian:
            next_state = "GREEN"

        try:
            self.light.set_state(next_state)
            self.current = next_state
        except Exception:
            logger.exception("Failed to set light state")

        payload = {"vehicles": vehicles, "pedestrian": pedestrian, "light_state": next_state}
        logger.info("Cycle", extra=payload)

        if self.network:
            try:
                self.network.publish("rakhsh/traffic/state", json.dumps(payload, ensure_ascii=False))
            except Exception:
                logger.exception("Network publish failed")
