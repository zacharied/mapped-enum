from enum import Enum

def enum_map(*args):
    def inner(cls):
        if not issubclass(cls, Enum):
            raise ValueError(f'{cls} is not a descendant of Enum')

        for index, arg in enumerate(args):
            # The i=index is done to capture the value of i, since defaults are captured at function declaration.
            def mapto(e, i=index):
                return e.value[i]

            # Same thing here.
            def mapfrom(k, i=index):
                for m in cls:
                    if m.value[i] == k:
                        return m

            if not hasattr(cls, f'to_{arg}'):
                setattr(cls, f'to_{arg}', mapto)
            if not hasattr(cls, f'from_{arg}'):
                setattr(cls, f'from_{arg}', mapfrom)

        return cls
    return inner
