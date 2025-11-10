import random

class SensorInterface:
    def __init__(self, simulation=True):
        self.simulation = simulation

    def get_sensor_data(self):
        """Считывает данные с датчиков движения и пешеходных кнопок"""
        if self.simulation:
            data = {
                "vehicles": random.randint(0, 10),
                "pedestrian": random.choice([True, False])
            }
        else:
            # Здесь будет код чтения с реальных сенсоров (через UART, Modbus и т.д.)
            data = {
                "vehicles": 0,   # Заглушка
                "pedestrian": False
            }
        return data
