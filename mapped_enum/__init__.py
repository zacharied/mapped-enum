from enum import Enum
import re

identifier_regex = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
map_key_regex = re.compile(r'[A-Za-z0-9_]+')


def enum_map(keys, to_prefix='to_', from_prefix='from_'):
    """
    Map the values of enum members to keywords for clear and concise conversions to and lookups from those keys. Each
    enum member must have a tuple value with a length equal to the number of space-separated keywords defined in the
    `keys` parameter.

    For each space-separated key specified in the `keys` parameter, a method called `to_<key>` and a class method called
    `from_<key>` will be added to the enum. These convert to and from the enum values at the index of the keyword. For
    example, given a mapped enum `Events` created with keys `'day month'` and a single member `BIRTHDAY = 11, 'august'`,
    a call to `Events.BIRTHDAY.to_day()` would return `11` and `Events.BIRTHDAY.to_month()` would return `'august'`.
    Likewise, a call to `Events.from_day(11)` would return `Events.BIRTHDAY`. Details on the generated methods are
    provided below.

    `to_<key>` is called on an enum member and takes no arguments. It returns the indexed member of the enum value tuple
    corresponding to the index of the `key`word.

    `from_<key>` is called directly on the enum class. It takes a single argument, the value to search for enum members
    with the value index corresponding to the index of the `key`word. If there is no enum member that satisfies the
    requested value, it will return `None`.

    :param keys: A single string containing a space-separated series of keys.
    :param to_prefix: An alternative prefix for the conversion methods instead of `to_`.
    :param from_prefix: An alternative prefix for the lookup methods instead of `from_`.
    :return: The decorated class.
    """
    keys = keys.replace('-', '_').split(' ')

    if keys[0] == '':
        raise ValueError('at least one key must be specified')

    for keyname in keys:
        if map_key_regex.match(keyname) is None:
            raise ValueError(f'key {keyname} results in invalid identifiers')

    def inner(cls):
        # Base constraint checking.
        if identifier_regex.match(to_prefix) is None:
            raise ValueError(f'invalid prefix "{to_prefix}" for `to` method')
        if identifier_regex.match(from_prefix) is None:
            raise ValueError(f'invalid prefix "{from_prefix}" for `from` method')
        if not issubclass(cls, Enum):
            raise ValueError(f'{cls} is not a descendant of Enum')

        cls._enum_map_tuples = {}
        for member in cls:
            cls._enum_map_tuples[member] = member.value if type(member.value) is tuple else (member.value,)
            if len(cls._enum_map_tuples[member]) != len(keys):
                raise AttributeError(f'{member} has the wrong number of map values (expected {len(keys)},'
                                     f'got {len(cls._enum_map_tuples[member])})')

        for index, arg in enumerate(keys):
            to_func = to_prefix + arg
            from_func = from_prefix + arg

            if not hasattr(cls, to_func):
                # The i=index is done to capture the value of i, since defaults are captured at function declaration.
                def mapto(e, i=index):
                    return cls._enum_map_tuples[e][i]

                setattr(cls, to_func, mapto)

            if not hasattr(cls, from_func):
                # Same thing here.
                def mapfrom(kls, k, i=index):
                    for m in kls:
                        if cls._enum_map_tuples[m][i] == k:
                            return m

                setattr(cls, from_func, classmethod(mapfrom))

        return cls

    return inner
