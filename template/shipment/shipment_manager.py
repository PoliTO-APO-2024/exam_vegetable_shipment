from typing import Callable, Optional, List
from shipment.elements import Vegetable
from shipment.exceptions import ShipmentException

class ShipmentManager:
    def __init__(self) -> None:
        pass

    # R1
    def add_vegetable(self, name: str, price_per_kg: float, heat_sensitivity: int, flavor_value: int) -> Vegetable:
        pass

    def add_city(self, name: str, value_fnc: Callable[[Vegetable, float], float]) -> None:
        pass

    def get_cities(self) -> List[str]:
        pass

    # R2
    def add_connection(self, city_name_1: str, city_name_2: str, delta_t: float) -> None:
        pass

    def get_connected(self, city_name: str) -> List[str]:
        pass

    def add_city_request(self, city_name: str, *vegetables: Vegetable) -> int:
        pass

    # R3
    def add_train_car(self, car_id: int, weight: int, *vegetables: Vegetable) -> None:
        pass

    def get_train_cars_for_cities(self) -> dict[str, List[int]]:
        pass

    # R4
    def get_temp_increment(self, city_start_name: str, city_end_name: str) -> Optional[float]:
        pass

    # R5
    def get_train_car_value(self, car_id, city_name, start_city = None):
        pass

    def get_best_deal(self, car_id):
        pass
