from enum import Enum
from functools import partial, partialmethod
import re

identifier_regex = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
map_key_regex = re.compile(r'[A-Za-z0-9_]+')


def enum_map(keys, to_prefix='to_', from_prefix='from_', allow_override=False):
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
    :param allow_override: If True, if the enum defines methods with the same name as a possible `enum_map` method, the
    `enum_map` method will be silently overridden. Otherwise, an error will be thrown.
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

        # Construct the mappings.
        cls._enum_map_tuples = {}
        for member in cls:
            # Convert the value to a tuple if there is only one value per enum member.
            cls._enum_map_tuples[member] = member.value if type(member.value) is tuple else (member.value,)

            # Ensure each member has the right number of keys.
            if len(cls._enum_map_tuples[member]) != len(keys):
                raise AttributeError(f'{member} has the wrong number of map values (expected {len(keys)}, '
                                     f'got {len(cls._enum_map_tuples[member])})')

        # Generate the `to` and `from` functions for each map key.
        for index, arg in enumerate(keys):
            to_func = to_prefix + arg
            from_func = from_prefix + arg

            if hasattr(cls, to_func):
                if not allow_override:
                    raise ValueError(f'the method "{to_func}" already exists')
            else:
                # We provide i as a keyword argument so we can capture it later using `partialmethod`.
                def mapto(e, i=-1):
                    return cls._enum_map_tuples[e][i]
                setattr(cls, to_func, partialmethod(mapto, i=index))

            if hasattr(cls, from_func):
                if not allow_override:
                    raise ValueError(f'the method "{from_func}" already exists')
            else:
                # The same technique as above is used for i here, except we capture it with `partial` instead.
                def mapfrom(kls, k, i=-1):
                    try:
                        return next(m for m in kls if cls._enum_map_tuples[m][i] == k)
                    except StopIteration:
                        return None
                setattr(cls, from_func, classmethod(partial(mapfrom, i=index)))

        return cls

    return inner
