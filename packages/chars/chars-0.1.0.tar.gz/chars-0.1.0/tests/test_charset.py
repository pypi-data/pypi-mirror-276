import unittest
from charset_project import charset

class TestChars(unittest.TestCase):
    def test_uppercase(self):
        self.assertEqual(charset.uppercase(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_lowercase(self):
        self.assertEqual(charset.lowercase(), "abcdefghijklmnopqrstuvwxyz")

    def test_numbers(self):
        self.assertEqual(charset.numbers(), "1234567890")

    def test_specialchars(self):
        self.assertEqual(charset.specialchars(), "~`!@#$%^&*()-_=+|[]\\{|};':\",./<> ?")

    def test_all(self):
        self.assertEqual(charset.all(), "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~`!@#$%^&*()-_=+|[]\\{|};':\",./<>? 1234567890")

if __name__ == '__main__':
    unittest.main()
