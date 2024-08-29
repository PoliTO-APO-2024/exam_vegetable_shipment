from shipment.shipment_manager import ShipmentManager
from shipment.exceptions import ShipmentException

EVAL_FNC_1 = lambda veg, temp: (veg.price_per_kg *(1 - veg.heat_sensitivity/10 * temp))
EVAL_FNC_2 = lambda veg, temp: (veg.price_per_kg *(1 + veg.flavor_value/10 - veg.heat_sensitivity/10 * temp))

def main():
    print("------------------------- R1 -------------------------")
    mg = ShipmentManager()
    carrot = mg.add_vegetable("Carrot", 0.86, 6, 9)
    
    print(carrot.name)                  # Carrot
    print(carrot.price_per_kg)          # 0.86
    print(carrot.heat_sensitivity)      # 6
    print(carrot.flavor_value)          # 9
    print(carrot)                       # Carrot 0.9 6 9

    mg.add_city("Los Angeles", EVAL_FNC_1)
    mg.add_city("San Diego", EVAL_FNC_2)
    mg.add_city("New York", EVAL_FNC_1)
    mg.add_city("Orlando", EVAL_FNC_2)
    mg.add_city("Denver", EVAL_FNC_1)

    print(mg.get_cities())   # ['Denver', 'Los Angeles', 'New York', 'Orlando', 'San Diego'] (ordine è importante)

    try:
        mg.add_city("Denver", EVAL_FNC_1)
        print("[ERROR] Creation of duplicated city not identified")
    except ShipmentException:
        print("Creation of duplicated city correctly identified")   # Creation of duplicated city correctly identified
    
    print("------------------------- R2 -------------------------")
    onion = mg.add_vegetable("Onion", 0.55, 2, 5)
    eggplant = mg.add_vegetable("Eggplant", 0.92, 8, 3)

    mg.add_connection("Los Angeles", "San Diego", 0.1)
    mg.add_connection("San Diego", "Denver", 0.5)
    mg.add_connection("Denver", "New York", 0.9)
    mg.add_connection("San Diego", "Orlando", 0.1)

    print(mg.get_connected("San Diego"))    # ['Orlando', 'Denver'] (ordine è importante)
    print(mg.get_connected("Orlando"))      # []  

    print(mg.add_city_request("New York", carrot, onion))       # 2
    print(mg.add_city_request("New York", carrot, eggplant))    # 1

    print("------------------------- R3 -------------------------")
    mg.add_city_request("Orlando", onion, eggplant)
    mg.add_city_request("New York", eggplant)

    mg.add_train_car(1, 400, onion)
    mg.add_train_car(2, 500, carrot)
    mg.add_train_car(3, 600, carrot, onion)

    print(mg.get_train_cars_for_cities())  # {'New York': [1, 2, 3], 'Orlando': [1, 3]} (ordine nelle liste è importante)

    print("------------------------- R4 -------------------------")
    print("{:.1f}".format(mg.get_temp_increment("Los Angeles", "New York")))   # 1.5
    print("{:.1f}".format(mg.get_temp_increment("San Diego", "New York")))     # 1.4
    print(mg.get_temp_increment("Denver", "Orlando"))                          # None

    print("------------------------- R5 -------------------------")
    print("{:.3f}".format(mg.get_train_car_value(3, "New York")))                   # 423.000
    print("{:.3f}".format(mg.get_train_car_value(3, "New York", "Los Angeles")))    # 141.300
    print("{:.3f}".format(mg.get_best_deal(3)))                                     # 737.700


if __name__ == "__main__":
    main()
