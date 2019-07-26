from mapped_enum import enum_map
from enum import Enum

import unittest


# TODO Use `assertRaisesRegex` instead of just `assertRegex`.
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

    def test_invalid_keynames(self):
        def raises():
            # noinspection PyUnusedLocal
            @enum_map('!bar')
            class Foo:
                pass

        self.assertRaises(ValueError, raises)

    def test_alternate_prefix(self):
        @enum_map('direction', to_prefix='as_', from_prefix='with_')
        class Cardinal(Enum):
            NORTH = 'up'
            WEST = 'left'

        self.assertEqual(Cardinal.NORTH.as_direction(), 'up')
        self.assertEqual(Cardinal.with_direction('left'), Cardinal.WEST)

    def test_wrong_alternate_prefix(self):
        def raises():
            # noinspection PyUnusedLocal
            @enum_map('name', to_prefix='1to_')
            class Foo(Enum):
                pass

        self.assertRaises(ValueError, raises)

    def test_no_keys(self):
        def raises():
            # noinspection PyUnusedLocal
            @enum_map('')
            class Foo(Enum):
                pass

        self.assertRaises(ValueError, raises)

    def test_wrong_mapping_count(self):
        def raises():
            # noinspection PyUnusedLocal
            @enum_map('speed color noise')
            class Car(Enum):
                RACECAR = 'fast', 'red', 'loud'
                # Missing `noise` mapping
                HYBRID = 'slow', 'blue'

        self.assertRaises(AttributeError, raises)

        def raises():
            # noinspection PyUnusedLocal
            @enum_map('speed')
            class Car(Enum):
                RACECAR = 'fast'
                # Has extra mapping
                HYBRID = 'slow', 'blue'

        self.assertRaises(AttributeError, raises)


if __name__ == '__main__':
    unittest.main()
