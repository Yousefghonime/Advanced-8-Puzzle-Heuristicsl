import unittest
from src.algorithms import a_star_search

class TestPuzzle(unittest.TestCase):
    def test_simple_solve(self):
        # حالة سهلة تحتاج حركة واحدة
        start = (1, 0, 2, 3, 4, 5, 6, 7, 8)
        result = a_star_search(start)
        self.assertEqual(result, ['LEFT'])

if __name__ == '__main__':
    unittest.main()