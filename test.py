from mapped_enum import enum_map
from enum import Enum

import unittest


class TestMapping(unittest.TestCase):
    def setUp(self):
        @enum_map(['color', 'sound'])
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
        with self.assertRaisesRegex(ValueError, 'not a descendant of Enum$'):
            # noinspection PyUnusedLocal
            @enum_map(['bar'])
            class Foo:
                pass

    def test_invalid_keynames(self):
        with self.assertRaisesRegex(ValueError, 'results in invalid identifiers$'):
            # noinspection PyUnusedLocal
            @enum_map(['!bar'])
            class Foo:
                pass

    def test_alternate_prefix(self):
        @enum_map(['direction'], to_prefix='as_', from_prefix='with_')
        class Cardinal(Enum):
            NORTH = 'up'
            WEST = 'left'

        self.assertEqual(Cardinal.NORTH.as_direction(), 'up')
        self.assertEqual(Cardinal.with_direction('left'), Cardinal.WEST)

    def test_wrong_alternate_prefix(self):
        with self.assertRaisesRegex(ValueError, '^invalid prefix ".*" for `to` method$'):
            # noinspection PyUnusedLocal
            @enum_map(['name'], to_prefix='1to_')
            class Foo(Enum):
                pass

    def test_no_keys(self):
        with self.assertRaisesRegex(ValueError, '^keys specifier cannot be empty$'):
            # noinspection PyUnusedLocal
            @enum_map('')
            class Foo(Enum):
                pass

        with self.assertRaisesRegex(ValueError, '^at least one key must be specified'):
            # noinspection PyUnusedLocal
            @enum_map([])
            class Foo(Enum):
                pass

    def test_wrong_mapping_count(self):
        with self.assertRaisesRegex(AttributeError, '^.* has the wrong number of map values'):
            # noinspection PyUnusedLocal
            @enum_map(['speed', 'color', 'noise'])
            class Car(Enum):
                RACECAR = 'fast', 'red', 'loud'
                # Missing `noise` mapping
                HYBRID = 'slow', 'blue'

        with self.assertRaisesRegex(AttributeError, '^.* has the wrong number of map values'):
            # noinspection PyUnusedLocal
            @enum_map(['speed'])
            class Car(Enum):
                RACECAR = 'fast'
                # Has extra mapping
                HYBRID = 'slow', 'blue'

    def test_override(self):
        with self.assertRaisesRegex(ValueError, 'already exists$'):
            # noinspection PyUnusedLocal
            @enum_map(['first_month', 'color'])
            class Season(Enum):
                SPRING = 'march', 'green'
                SUMMER = 'july', 'yellow'
                FALL = 'september', 'orange'
                WINTER = 'december', 'blue'

                def to_color(self):
                    # This method being defined should cause an exception.
                    pass

        @enum_map(['first_month', 'color'], allow_override=True)
        class Season(Enum):
            SPRING = 'march', 'green'
            SUMMER = 'july', 'yellow'
            FALL = 'september', 'orange'
            WINTER = 'december', 'blue'

            def to_color(self):
                # Override Summer's color to be red instead.
                if self == self.SUMMER:
                    return 'red'
                return self.value[1]

        self.assertEqual(Season.WINTER.to_color(), 'blue')
        self.assertEqual(Season.SUMMER.to_color(), 'red')

    def test_multiple_froms(self):
        @enum_map(['ground', 'water'], multiple_from=True)
        class Environment(Enum):
            DESERT = 'sand', 'none'
            BEACH = 'sand', 'lots'
            PLAINS = 'grass', 'some'

        self.assertEqual(Environment.from_ground('sand'), [Environment.DESERT, Environment.BEACH])


if __name__ == '__main__':
    unittest.main()
