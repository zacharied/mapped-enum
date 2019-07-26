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

        cls._enum_map_tuple_key = len(keys) != 1

        if not issubclass(cls, Enum):
            raise ValueError(f'{cls} is not a descendant of Enum')

        for member in list(cls):
            if cls._enum_map_tuple_key and len(member.value) != len(keys) \
                    or not cls._enum_map_tuple_key and type(member.value) is tuple:
                raise AttributeError(f'{member} has the wrong number of map values')

        for index, arg in enumerate(keys):
            to_func = to_prefix + arg
            from_func = from_prefix + arg

            if not hasattr(cls, to_func):
                # TODO Are these methods added before or after the class has been initialized?
                # The i=index is done to capture the value of i, since defaults are captured at function declaration.
                def mapto(e, i=index):
                    return e.value[i] if cls._enum_map_tuple_key else e.value

                setattr(cls, to_func, mapto)

            if not hasattr(cls, from_func):
                # Same thing here.
                def mapfrom(kls, k, i=index):
                    for m in kls:
                        if (m.value[i] if cls._enum_map_tuple_key else m.value) == k:
                            return m

                setattr(cls, from_func, classmethod(mapfrom))

        return cls

    return inner
