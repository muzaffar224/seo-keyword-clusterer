import unittest
from keyword_clusterer.core import cluster, intent, normalize, signature

class KeywordClustererTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize("  Greggs'  Prices! "), "greggs prices")
    def test_equivalent_price_modifiers(self):
        self.assertEqual(signature("greggs price"), signature("greggs cost"))
    def test_distinct_intents(self):
        self.assertNotEqual(signature("greggs price"), signature("greggs calories"))
    def test_deduplicate_and_order(self):
        result = cluster([
            {"keyword": "greggs price", "volume": 100},
            {"keyword": "GREGGS PRICE", "volume": 120},
            {"keyword": "greggs cost", "volume": 80},
            {"keyword": "greggs calories", "volume": 200},
        ])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["main_keyword"], "greggs calories")
        self.assertEqual(result[1]["group_id"], result[2]["group_id"])
    def test_intent(self):
        self.assertEqual(intent("opening hours"), "hours")

if __name__ == "__main__":
    unittest.main()
