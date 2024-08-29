from typing import Callable, Optional, List
from shipment.elements import Vegetable, City, TrainCar
from shipment.exceptions import ShipmentException

class ShipmentManager:
    def __init__(self) -> None:
        self._vegetables = {}
        self._cities = {}
        self._train_cars = {}

    # R1
    def add_vegetable(self, name: str, price_per_kg: float, heat_sensitivity: int, flavor_value: int) -> Vegetable:
        veg = Vegetable(name, price_per_kg, heat_sensitivity, flavor_value)
        self._vegetables[name] = veg
        return veg

    def add_city(self, name: str, value_fnc: Callable[[Vegetable, float], float]) -> None:
        if name in self._cities:
            raise ShipmentException("Adding duplicated city")
        self._cities[name] = City(name, value_fnc)

    def get_cities(self) -> List[str]:
        return sorted(self._cities.keys())

    # R2
    def add_connection(self, city_name_1: str, city_name_2: str, delta_t: float) -> None:
        city_1 = self._cities[city_name_1]
        city_2 = self._cities[city_name_2]
        city_1.add_connection(city_2, delta_t)

    def get_connected(self, city_name: str) -> List[str]:
        return [c[0].name for c in sorted(self._cities[city_name].connections.values(), key=lambda x: x[1])]

    def add_city_request(self, city_name: str, *vegetables: Vegetable) -> int:
        return self._cities[city_name].add_requested(*[v.name for v in vegetables])

    # R3
    def add_train_car(self, car_id: int, weight: int, *vegetables: Vegetable) -> None:
        self._train_cars[car_id] = TrainCar(car_id, weight, *[v.name for v in vegetables])
    
    def get_train_cars_for_cities(self) -> dict[str, List[int]]:
        city_dict = {}
        for city in self._cities.values():
            requested = city.requested
            train_car_list = []
            for train_car in self._train_cars.values():
                transported = train_car.vegetable_names
                if transported.intersection(requested):
                    train_car_list.append(train_car.car_id)
            if train_car_list:
                city_dict[city.name] = sorted(train_car_list)
        return city_dict

    # R4
    def get_temp_increment(self, city_start_name: str, city_end_name: str) -> Optional[float]:
        temp_increase = 0
        city_start = self._cities[city_start_name]
        city_end = self._cities[city_end_name]
        return self._depth_first(city_start, city_end, 0, 0)

    # R5
    def get_train_car_value(self, car_id, city_name, start_city = None):
        eval_fnc = self._cities[city_name].eval_fnc
        train_car = self._train_cars[car_id]
        vegetables = [self._vegetables[name] for name in train_car.vegetable_names]
        temp = self.get_temp_increment(start_city, city_name) if start_city is not None else 0
        prices = [eval_fnc(v, temp) for v in vegetables]
        tot_price = sum(prices)/len(prices) * train_car.weight
        return tot_price

    def get_best_deal(self, car_id):
        best_price = -1
        for city_name in self._cities:
            price = self.get_train_car_value(car_id, city_name)
            if price > best_price:
                best_price = price
        return best_price

    # support
    def _depth_first(self, current_city, final_city, temp_incr, temp_tot):
        temp_tot = temp_tot + temp_incr
        if current_city == final_city:
            return temp_tot
            
        for city, temp in current_city.connections.values():
            ret = self._depth_first(city, final_city, temp, temp_tot)
            if ret:
                return ret
        return None
