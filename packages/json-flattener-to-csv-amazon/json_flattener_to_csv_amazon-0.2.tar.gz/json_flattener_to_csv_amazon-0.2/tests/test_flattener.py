# tests/test_flattener.py
import unittest
from json_flattener_to_csv_amazon import flatten_json

class TestFlattener(unittest.TestCase):
    def test_flatten_json(self):
        json_data = [
            {
                "portfolioId": 269621039628866,
                "name": "US-24FT-OM-PT",
                "budget": {
                    "amount": 1.0,
                    "currencyCode": "USD",
                    "policy": "dateRange",
                    "startDate": "20240529",
                    "endDate": "20240529"
                },
                "inBudget": True,
                "state": "enabled"
            },
            {
                "portfolioId": 165380338689037,
                "name": "US-54FMT-SP-BROAD-ROOT",
                "budget": {
                    "amount": 5.0,
                    "currencyCode": "USD",
                    "policy": "dateRange",
                    "startDate": "20240529",
                    "endDate": "20240529"
                },
                "inBudget": True,
                "state": "enabled"
            }
        ]
        
        df = flatten_json(json_data)
        self.assertEqual(df.shape, (2, 8))
        self.assertIn('budget.amount', df.columns)
        self.assertIn('budget.currencyCode', df.columns)

if __name__ == '__main__':
    unittest.main()
