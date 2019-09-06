from enum import Enum
import re

KWARGS_PARAM_TO_PREFIX = 'to_prefix'
KWARGS_PARAM_FROM_PREFIX = 'from_prefix'

identifier_regex = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
map_key_regex = re.compile(r'[A-Za-z0-9_]+')


def enum_map(keys, **kwargs):
    # TODO Documentation
    keys = keys.replace('-', '_').split(' ')

    if keys[0] == '':
        raise ValueError('at least one key must be specified')

    for keyname in keys:
        if map_key_regex.match(keyname) is None:
            raise ValueError(f'key {keyname} results in invalid identifiers')

    def inner(cls):
        if KWARGS_PARAM_TO_PREFIX in kwargs:
            if identifier_regex.match(kwargs[KWARGS_PARAM_TO_PREFIX]) is None:
                raise ValueError(f'invalid prefix {kwargs[KWARGS_PARAM_TO_PREFIX]} for `to` method')
        if KWARGS_PARAM_FROM_PREFIX in kwargs:
            if identifier_regex.match(kwargs[KWARGS_PARAM_FROM_PREFIX]) is None:
                raise ValueError(f'invalid prefix {kwargs[KWARGS_PARAM_FROM_PREFIX]} for `from` method')

        to_prefix = 'to_' if KWARGS_PARAM_TO_PREFIX not in kwargs else kwargs[KWARGS_PARAM_TO_PREFIX]
        from_prefix = 'from_' if KWARGS_PARAM_FROM_PREFIX not in kwargs else kwargs[KWARGS_PARAM_FROM_PREFIX]

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
