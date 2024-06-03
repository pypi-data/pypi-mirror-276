import unittest


# Replace 'your_module' with the name of the module where the add function is defined
from pypi_cicd.pypi_cicd import add


class TestAddFunction(unittest.TestCase):

    def test_add_positive_numbers(self):
        self.assertEqual(add(1, 2), 3)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

    def test_add_zero(self):
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(0, 5), 5)
        self.assertEqual(add(5, 0), 5)

    def test_add_positive_and_negative(self):
        self.assertEqual(add(10, -10), 0)
        self.assertEqual(add(-5, 5), 0)


if __name__ == '__main__':
    unittest.main()
