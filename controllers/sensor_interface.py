# Симуляция датчиков движения
import random

def get_vehicle_count():
    return random.randint(0, 20)

def get_pedestrian_count():
    return random.randint(0, 10)

if __name__ == "__main__":
    print("Транспорт:", get_vehicle_count())
    print("Пешеходы:", get_pedestrian_count())
