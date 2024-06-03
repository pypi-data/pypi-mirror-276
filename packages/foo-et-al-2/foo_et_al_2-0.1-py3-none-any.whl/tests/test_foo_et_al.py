import unittest
from foo_et_al.foo_et_al import foo_et_al_param
from math import pi as PI

class TestFooEtAl(unittest.TestCase):
    def test_foo_et_al_param(self):
        """Tests the foo.foo_et_al_param method."""

        for r in range(0, 5):
            expected_result = 4 / 3 * PI * r ** 3
            try:
                self.assertEqual(foo_et_al_param(r), expected_result)
            except AssertionError:
                print(f"Failure on foo_et_al_param(radius = {r})")
                raise
        
        # Test for r = None
        self.assertRaises(ValueError, foo_et_al_param, None)

        # Test for r < 0
        self.assertRaises(ValueError, foo_et_al_param, -1)


if __name__ == '__main__':
    unittest.main()