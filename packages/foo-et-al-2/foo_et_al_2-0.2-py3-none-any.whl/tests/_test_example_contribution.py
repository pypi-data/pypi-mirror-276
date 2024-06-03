import unittest
from et_al._example_contribution.hello_world import hello_world
from et_al._example_contribution.is_palindrome import is_palindrome

class TestExampleContribution(unittest.TestCase):
    def test_hello_world(self):
        """Tests the _example_contribution.hello_world method."""

        self.assertEqual(hello_world(), "Hello, world!")

    def test_is_palindrome(self):
        """Tests the _example_contribution.is_palindrome method."""

        self.assertTrue(is_palindrome("racecar"))
        self.assertFalse(is_palindrome("UCAR"))

if __name__ == '__main__':
    unittest.main()