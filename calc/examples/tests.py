import unittest
from resistors import *

class TestFunctions(unittest.TestCase):
    def test_preferred_closest(self):
        self.assertTrue(preferred_closest(15) == 15)
        self.assertTrue(preferred_closest(150) == 150)
        self.assertTrue(preferred_closest(47) == 47)
        self.assertTrue(preferred_closest(54) == 56)
        self.assertTrue(preferred_closest(90) == 82)
        self.assertTrue(preferred_closest(218) == 220)
        self.assertTrue(preferred_closest(465) == 470)
        self.assertTrue(preferred_closest(5100.0, "E24") == 5100)

    def test_divider(self):
        self.assertTrue(design_div(10, 0, 5, 1000) == (2000.0, 2000.0))

    def test_rationalize(self):
        self.assertEqual(rationalize(5454.545454545455, mixed=False), Rat(0,60000,11))
        self.assertEqual(rationalize(5454.545454545455).int_part, 5454)
        self.assertEqual(rationalize(5454.545454545455) , Rat(0,60000,11))
        self.assertEqual(rationalize(5882.352941176471, mixed=False) , Rat(0,100000,17))
        self.assertEqual(rationalize(5882.352941176471) , Rat(0,100000,17))
        self.assertEqual(rationalize(5882.352941176471).int_part , 5882)
        self.assertEqual(rationalize(28) , Rat(28,0,1))

if __name__ == "__main__":
    # run_tests()
    unittest.main()
    exit(0)
