import unittest
from calculator import calculate_total


class CalculatorTests(unittest.TestCase):
    def test_positive_amount(self):
        self.assertEqual(calculate_total(100, 10), 110)

    def test_zero_tax(self):
        self.assertEqual(calculate_total(50, 0), 50)

    def test_negative_adjustment(self):
        self.assertEqual(calculate_total(-10, 2), -8)


if __name__ == "__main__":
    unittest.main()
