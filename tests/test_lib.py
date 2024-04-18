import unittest

from lib.api.fofa.pack import FofaSearch


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


class TestDork(unittest.TestCase):
    def test_fofa(self):
        results = FofaSearch("http", limit=100, offset=0)
        self.assertIsNotNone(results)



if __name__ == '__main__':
    unittest.main()
