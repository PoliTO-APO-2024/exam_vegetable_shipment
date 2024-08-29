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
        pass
    