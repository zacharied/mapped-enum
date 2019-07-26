from enum import Enum

def enum_map(*args):
    # TODO Documentation
    def inner(cls):
        if not issubclass(cls, Enum):
            raise ValueError(f'{cls} is not a descendant of Enum')

        for index, arg in enumerate(args):
            if not hasattr(cls, f'to_{arg}'):
                # TODO Are these methods added before or after the class has been initialized?
                # The i=index is done to capture the value of i, since defaults are captured at function declaration.
                def mapto(e, i=index):
                    return e.value[i]

                setattr(cls, f'to_{arg}', mapto)

            if not hasattr(cls, f'from_{arg}'):
                # Same thing here.
                def mapfrom(kls, k, i=index):
                    for m in kls:
                        if m.value[i] == k:
                            return m

                setattr(cls, f'from_{arg}', classmethod(mapfrom))

        return cls

    return inner
