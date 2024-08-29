class Vegetable:
    def __init__(self, name: str, price_per_kg: float, heat_sensitivity: int, flavor_value: int) -> None:
        self._name = name
        self._price_per_kg = price_per_kg
        self._heat_sensitivity = heat_sensitivity
        self._flavor_value = flavor_value
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def price_per_kg(self) -> float:
        return self._price_per_kg

    @property
    def heat_sensitivity(self) -> int:
        return self._heat_sensitivity

    @property
    def flavor_value(self) -> int:
        return self._flavor_value

    def __repr__(self) -> str:
        return "{} {:.1f} {} {}".format(self.name, self.price_per_kg, self.heat_sensitivity, self.flavor_value)


class City:
    def __init__(self, name, eval_fnc):
        self._name = name
        self._eval_fnc = eval_fnc
        self._connections = {}
        self._requested = set()

    @property
    def name(self):
        return self._name

    @property
    def eval_fnc(self):
        return self._eval_fnc
    
    def add_connection(self, city, delta_t):
        self._connections[city.name] = (city, delta_t)

    @property
    def connections(self):
        return self._connections

    def add_requested(self, *vegetable_names):
        vegetable_names = set(vegetable_names)
        num_added = len(vegetable_names.difference(self._requested))
        self._requested = self._requested.union(vegetable_names)
        return num_added

    @property
    def requested(self):
        return self._requested


class TrainCar:
    def __init__(self, car_id, weight, *vegetable_names):
        self._car_id = car_id
        self._weight = weight
        self._vegetable_names = set(vegetable_names)

    @property
    def car_id(self):
        return self._car_id
    
    @property
    def weight(self):
        return self._weight

    @property
    def vegetable_names(self):
        return self._vegetable_names




