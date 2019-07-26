from mapped_enum import enum_map
from enum import Enum

import unittest

class TestMapping(unittest.TestCase):
    def setUp(self):
        @enum_map('color', 'sound')
        class Animal(Enum):
            CHOCOLATE_LAB = 'brown', 'woof'
            TABBY_CAT = 'orange', 'meow'
            LION = 'yellow', 'roar'
        self.Animal = Animal

    def test_to(self):
        self.assertEqual(self.Animal.CHOCOLATE_LAB.to_color(), 'brown')
        self.assertEqual(self.Animal.TABBY_CAT.to_sound(), 'meow')

    def test_from(self):
        self.assertEqual(self.Animal.from_color('yellow'), self.Animal.LION)
        self.assertEqual(self.Animal.from_sound('woof'), self.Animal.CHOCOLATE_LAB)

    def test_non_enum(self):
        def raises():
            # noinspection PyUnusedLocal
            @enum_map('bar')
            class Foo:
                pass

        self.assertRaises(ValueError, raises)

if __name__ == '__main__':
    unittest.main()