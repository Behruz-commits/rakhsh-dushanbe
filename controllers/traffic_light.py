# Управление светофором на перекрёстке
import time

class TrafficLight:
    def __init__(self, intersection_id):
        self.intersection_id = intersection_id
        self.state = "RED"

    def change_state(self, new_state):
        print(f"[{self.intersection_id}] Светофор меняет состояние: {self.state} -> {new_state}")
        self.state = new_state

    def run_cycle(self):
        while True:
            self.change_state("GREEN")
            time.sleep(5)
            self.change_state("YELLOW")
            time.sleep(2)
            self.change_state("RED")
            time.sleep(5)

if __name__ == "__main__":
    tl = TrafficLight("Crossroad-1")
    tl.run_cycle()
