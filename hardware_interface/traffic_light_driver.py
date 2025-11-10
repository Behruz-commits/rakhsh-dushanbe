import time

class TrafficLightDriver:
    def __init__(self, simulation=True):
        self.simulation = simulation
        self.state = "RED"

    def set_light_state(self, state):
        """Управление состоянием светофора"""
        self.state = state
        if self.simulation:
            print(f"[СИМУЛЯТОР] Светофор переключён в {state}")
        else:
            # Здесь подключается реальный контроллер (через GPIO, Modbus, RS485)
            print(f"[ОБОРУДОВАНИЕ] Установка состояния ламп: {state}")

    def get_state(self):
        return self.state
