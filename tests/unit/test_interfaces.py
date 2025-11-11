# path: tests/unit/test_interfaces.py
import unittest
from core.interfaces import ILightDriver, ISensor
class DummyLight:
    def __init__(self):
        self.s = "RED"
    def set_state(self, state):
        self.s = state
    def get_state(self):
        return self.s

class DummySensor:
    def read(self):
        return {"vehicles": 1, "pedestrian": False}

class TestContracts(unittest.TestCase):
    def test_light_protocol(self):
        l = DummyLight()
        assert isinstance(l.get_state(), str)
        l.set_state("GREEN")
        self.assertEqual(l.get_state(), "GREEN")

    def test_sensor_protocol(self):
        s = DummySensor()
        self.assertIn("vehicles", s.read())

if __name__ == "__main__":
    unittest.main()
