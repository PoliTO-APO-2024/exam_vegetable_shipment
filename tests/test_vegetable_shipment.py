import unittest
from shipment.shipment_manager import ShipmentManager, ShipmentException


class TestR1(unittest.TestCase):
    def setUp(self):
        self._mg = ShipmentManager()

    def test_add_vegetable_multiple(self):
        veg1 = self._mg.add_vegetable("veg1", 0.945, 4, 7)
        veg2 = self._mg.add_vegetable("veg2", 1.41, 7, 9)
        self.assertEqual("veg1", veg1.name)
        self.assertEqual("veg2", veg2.name)

    def test_vegetable_properties(self):
        veg1 = self._mg.add_vegetable("veg1", 0.945, 4, 7)
        self.assertEqual("veg1", veg1.name)
        self.assertAlmostEqual(0.945, veg1.price_per_kg)
        self.assertEqual(4, veg1.heat_sensitivity)
        self.assertEqual(7, veg1.flavor_value)

    def test_repr(self):
        veg1 = self._mg.add_vegetable("veg1", 0.945, 4, 7)
        self.assertEqual("veg1 0.9 4 7", str(veg1))
    
    def test_get_cities(self):
        self._mg.add_city("city3", lambda x, y: 0)
        self._mg.add_city("city1", lambda x, y: 0)
        self._mg.add_city("city2", lambda x, y: 0)
        self.assertEqual(["city1", "city2", "city3"], self._mg.get_cities())

    def test_add_city_exception(self):
        self._mg.add_city("city3", lambda x, y: 0)
        self.assertRaises(ShipmentException, self._mg.add_city, "city3", lambda x, y: 0)


class TestR2(unittest.TestCase):
    def setUp(self):
        self._mg = ShipmentManager()
        self._mg.add_city("city1", lambda x, y: 0)
        self._mg.add_city("city2", lambda x, y: 0)
        self._mg.add_city("city3", lambda x, y: 0)
        self._mg.add_city("city4", lambda x, y: 0)
        self._mg.add_city("city5", lambda x, y: 0)

        self._veg1 = self._mg.add_vegetable("veg1", 0, 0, 0)
        self._veg2 = self._mg.add_vegetable("veg2", 0, 0, 0)
        self._veg3 = self._mg.add_vegetable("veg3", 0, 0, 0)
        self._veg4 = self._mg.add_vegetable("veg4", 0, 0, 0)
        self._veg5 = self._mg.add_vegetable("veg5", 0, 0, 0)
    
    def test_get_connected(self):
        self._mg.add_connection("city1", "city2", 0.5)
        self._mg.add_connection("city1", "city3", 0.3)
        self._mg.add_connection("city1", "city4", 0.4)
        self._mg.add_connection("city2", "city5", 0.7)

        cities = self._mg.get_connected("city1")
        self.assertEqual(["city3", "city4", "city2"], cities)        

    def test_get_connected_empty(self):
        self._mg.add_connection("city1", "city2", 0.5)
        self._mg.add_connection("city1", "city3", 0.3)
        self._mg.add_connection("city1", "city4", 0.4)
        self._mg.add_connection("city2", "city5", 0.7)
        
        cities = self._mg.get_connected("city2")
        self.assertTrue(len(cities) != 0)

        cities = self._mg.get_connected("city3")
        self.assertTrue(len(cities) == 0)

    def test_add_city_request_single(self):
        ret = self._mg.add_city_request("city1", self._veg1, self._veg3, self._veg4)
        self.assertEqual(3, ret)
        ret = self._mg.add_city_request("city1", self._veg2, self._veg3, self._veg5)
        self.assertEqual(2, ret)

    def test_add_city_request_multiple(self):
        ret1 = self._mg.add_city_request("city1", self._veg1, self._veg3)
        ret2 = self._mg.add_city_request("city2", self._veg2)
        self.assertEqual(2, ret1)
        self.assertEqual(1, ret2)
        ret1 = self._mg.add_city_request("city1", self._veg1, self._veg3)
        ret2 = self._mg.add_city_request("city2", self._veg5, self._veg3)
        self.assertEqual(0, ret1)
        self.assertEqual(2, ret2)


class TestR3(unittest.TestCase):
    def setUp(self):
        self._mg = ShipmentManager()
        self._veg1 = self._mg.add_vegetable("veg1", 0, 0, 0)
        self._veg2 = self._mg.add_vegetable("veg2", 0, 0, 0)
        self._veg3 = self._mg.add_vegetable("veg3", 0, 0, 0)
        self._veg4 = self._mg.add_vegetable("veg4", 0, 0, 0)
        self._veg5 = self._mg.add_vegetable("veg5", 0, 0, 0)

    def test_get_train_cars_for_cities_simple(self):
        self._mg.add_city("city1", lambda x, y: 0)
        self._mg.add_city("city2", lambda x, y: 0)

        self._mg.add_city_request("city1", self._veg1, self._veg3)
        self._mg.add_city_request("city2", self._veg3, self._veg5)

        self._mg.add_train_car(1, 1000, self._veg1)
        self._mg.add_train_car(2, 1000, self._veg5, self._veg3)

        res_dict = self._mg.get_train_cars_for_cities()

        self.assertTrue("city1" in res_dict and "city2" in res_dict)
        self.assertEqual([1, 2], res_dict["city1"])
        self.assertEqual([2], res_dict["city2"])

    def test_get_train_cars_for_complex(self):
        self._mg.add_city("city1", lambda x, y: 0)
        self._mg.add_city("city2", lambda x, y: 0)

        self._mg.add_city_request("city1", self._veg1, self._veg2)
        self._mg.add_city_request("city2", self._veg3, self._veg5)       
        
        self._mg.add_train_car(5, 1000, self._veg2, self._veg3)
        self._mg.add_train_car(4, 1000, self._veg1, self._veg2, self._veg3)
        self._mg.add_train_car(3, 1000, self._veg3, self._veg4, self._veg5)
        self._mg.add_train_car(2, 1000, self._veg3)
        self._mg.add_train_car(1, 1000, self._veg1)

        res_dict = self._mg.get_train_cars_for_cities()

        self.assertTrue("city1" in res_dict and "city2" in res_dict)
        self.assertEqual([1, 4, 5], res_dict["city1"])
        self.assertEqual([2, 3, 4, 5], res_dict["city2"])

    def test_get_train_cars_for_cities_missing(self):
        self._mg.add_city("city1", lambda x, y: 0)
        self._mg.add_city("city2", lambda x, y: 0)
        self._mg.add_city("city3", lambda x, y: 0)
        self._mg.add_city("city4", lambda x, y: 0)

        self._mg.add_city_request("city2", self._veg2, self._veg4)
        self._mg.add_city_request("city2", self._veg1, self._veg3)
        self._mg.add_city_request("city4", self._veg3, self._veg5)

        self._mg.add_train_car(1, 1000, self._veg1)
        self._mg.add_train_car(2, 1000, self._veg5, self._veg3)

        res_dict = self._mg.get_train_cars_for_cities()
        self.assertEqual(set(["city2", "city4"]), set(res_dict.keys()))
        

class TestR4(unittest.TestCase):
    def setUp(self):
        self._mg = ShipmentManager()
        self._mg.add_city("city1", lambda x, y: 0)
        self._mg.add_city("city2", lambda x, y: 0)
        self._mg.add_city("city3", lambda x, y: 0)
        self._mg.add_city("city4", lambda x, y: 0)
        self._mg.add_city("city5", lambda x, y: 0)
        self._mg.add_city("city6", lambda x, y: 0)

        self._mg.add_connection("city1", "city2", 0.3)
        self._mg.add_connection("city2", "city3", 0.4)
        self._mg.add_connection("city2", "city4", 0.5)
        self._mg.add_connection("city2", "city5", 0.6)
        self._mg.add_connection("city5", "city6", 0.7)

    def test_get_temp_increment_root(self):
        self.assertAlmostEqual(1.6, self._mg.get_temp_increment("city1", "city6"))
        self.assertAlmostEqual(0.7, self._mg.get_temp_increment("city1", "city3"))

    def test_get_temperature_increase_middle(self):
        self.assertAlmostEqual(1.3, self._mg.get_temp_increment("city2", "city6"))
        self.assertAlmostEqual(0.5, self._mg.get_temp_increment("city2", "city4"))

    def test_get_temperature_increase_none(self):
        self.assertIsNotNone(self._mg.get_temp_increment("city1", "city4"))
        self.assertIsNone(self._mg.get_temp_increment("city3", "city4"))


class TestR5(unittest.TestCase):
    def setUp(self):
        eval_fnc1 = lambda veg, temp: (veg.price_per_kg *(1 - veg.heat_sensitivity/10 * temp))
        eval_fnc2 = lambda veg, temp: (veg.price_per_kg *(1 + veg.flavor_value/10 - veg.heat_sensitivity/10 * temp))

        self._mg = ShipmentManager()
        self._mg.add_city("city1", eval_fnc1)
        self._mg.add_city("city2", eval_fnc2)
        self._mg.add_city("city3", eval_fnc1)
        self._mg.add_city("city4", eval_fnc2)
        self._mg.add_city("city5", eval_fnc1)
        self._mg.add_city("city6", eval_fnc2)

        self._mg.add_connection("city1", "city2", 0.3)
        self._mg.add_connection("city2", "city3", 0.4)
        self._mg.add_connection("city2", "city4", 0.5)
        self._mg.add_connection("city2", "city5", 0.6)
        self._mg.add_connection("city5", "city6", 0.7)

        self._veg1 = self._mg.add_vegetable("veg1", 0.9, 4, 7)
        self._veg2 = self._mg.add_vegetable("veg2", 1.2, 5, 1)
        self._veg3 = self._mg.add_vegetable("veg3", 1.5, 8, 3)

        self._mg.add_city_request("city1", self._veg1, self._veg2, self._veg3)
        self._mg.add_city_request("city2", self._veg1, self._veg2)
        self._mg.add_city_request("city3", self._veg2, self._veg3)

        self._mg.add_train_car(1, 500, self._veg1, self._veg2, self._veg3)

    def test_get_train_car_value_no_temp(self):
        self.assertAlmostEqual(600, self._mg.get_train_car_value(1, "city3"))

    def test_get_train_car_value_temp(self):
        self.assertAlmostEqual(348, self._mg.get_train_car_value(1, "city3", "city1"))

    def test_get_best_deal(self):
        self.assertAlmostEqual(800, self._mg.get_best_deal(1))
        

