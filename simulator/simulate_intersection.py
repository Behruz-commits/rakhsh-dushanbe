# Симулятор перекрестка с интеграцией ЦУАК
from controllers.traffic_light import TrafficLight
from simulator.visualization import visualize
from controllers import sensor_interface

def run_simulation(intersection_id):
    tl = TrafficLight(intersection_id)
    while True:
        # Симулируем данные с датчиков
        vehicles = sensor_interface.get_vehicle_count()
        pedestrians = sensor_interface.get_pedestrian_count()
        
        # Обновляем светофор по простому правилу
        if vehicles > 10:
            tl.change_state("GREEN")
        elif pedestrians > 5:
            tl.change_state("GREEN")
        else:
            tl.change_state("RED")
        
        # Визуализация состояния
        visualize(intersection_id, tl.state)

if __name__ == "__main__":
    run_simulation("Sim-Crossroad")
