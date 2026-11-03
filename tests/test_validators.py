import unittest
from src.validators import transform_weather, DataValidationError
def payload():
    return {"name":"Test City","sys":{"country":"IN"},"coord":{"lat":19,"lon":72},"dt":1700000000,
            "main":{"temp":28.5,"feels_like":29,"humidity":65,"pressure":1012},
            "wind":{"speed":3.4},"weather":[{"main":"Clear","description":"clear sky"}]}
class ValidatorTests(unittest.TestCase):
    def test_valid_payload(self):
        o=transform_weather(payload(),fetched_at="2024-01-01T00:00:00Z")
        self.assertEqual(o["temperature_c"],28.5)
        self.assertTrue(o["observed_at"].endswith("Z"))
    def test_invalid_humidity(self):
        d=payload(); d["main"]["humidity"]=150
        with self.assertRaises(DataValidationError): transform_weather(d)
    def test_missing_weather(self):
        d=payload(); d["weather"]=[]
        with self.assertRaises(DataValidationError): transform_weather(d)
if __name__=="__main__": unittest.main()
