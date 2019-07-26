from mapped_enum import enum_map
from enum import Enum, auto

import unittest


class TestMapping(unittest.TestCase):
    def setUp(self):
        @enum_map('color sound')
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

    def test_alternate_prefix(self):
        @enum_map('direction', to_prefix='as_', from_prefix='with_')
        class Cardinal(Enum):
            NORTH = 'up'
            SOUTH = 'down'
            WEST = 'left'
            EAST = 'right'

        self.assertEqual(Cardinal.NORTH.as_direction(), 'up')
        self.assertEqual(Cardinal.with_direction('left'), Cardinal.WEST)

    def test_no_keys(self):
        def raises():
            # noinspection PyUnusedLocal
            @enum_map('')
            class Car(Enum):
                RACECAR = auto()
                SPORTSCAR = auto()
                SEDAN = auto()

        self.assertRaises(ValueError, raises)


if __name__ == '__main__':
    unittest.main()