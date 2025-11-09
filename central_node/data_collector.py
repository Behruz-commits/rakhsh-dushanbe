# Сбор данных с перекрёстков
from controllers import sensor_interface

def collect_data():
    vehicles = sensor_interface.get_vehicle_count()
    pedestrians = sensor_interface.get_pedestrian_count()
    data = {"vehicles": vehicles, "pedestrians": pedestrians}
    print("Собраны данные:", data)
    return data
