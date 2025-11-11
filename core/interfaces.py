# path: core/interfaces.py
from typing import Protocol, Dict, Any

class ILightDriver(Protocol):
    """Абстракция управления светофором."""
    def set_state(self, state: str) -> None: ...
    def get_state(self) -> str: ...

class ISensor(Protocol):
    """Абстракция сенсора (машины / пешеходы)."""
    def read(self) -> Dict[str, Any]: ...

class INetworkClient(Protocol):
    """Абстракция сети (MQTT/HTTP)."""
    def publish(self, topic: str, payload: str) -> None: ...
    def subscribe(self, topic: str, callback) -> None: ...

class IParkingSensor(Protocol):
    """Абстракция парковочных сенсоров / камеры."""
    def read_parking_status(self) -> Dict[str, Any]: ...
