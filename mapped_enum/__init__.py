from enum import Enum

KWARGS_PARAM_TO_PREFIX = 'to_prefix'
KWARGS_PARAM_FROM_PREFIX = 'from_prefix'

def enum_map(*args, **kwargs):
    # TODO Documentation
    def inner(cls):
        to_prefix = 'to_' if KWARGS_PARAM_TO_PREFIX not in kwargs else kwargs[KWARGS_PARAM_TO_PREFIX]
        from_prefix = 'from_' if KWARGS_PARAM_FROM_PREFIX not in kwargs else kwargs[KWARGS_PARAM_FROM_PREFIX]

        if not issubclass(cls, Enum):
            raise ValueError(f'{cls} is not a descendant of Enum')

        # TODO This doesn't work if there is only one map value.
        for index, arg in enumerate(args):
            to_func = to_prefix + arg
            from_func = from_prefix + arg

            if not hasattr(cls, to_func):
                # TODO Are these methods added before or after the class has been initialized?
                # The i=index is done to capture the value of i, since defaults are captured at function declaration.
                def mapto(e, i=index):
                    return e.value[i]

                setattr(cls, to_func, mapto)

            if not hasattr(cls, from_func):
                # Same thing here.
                def mapfrom(kls, k, i=index):
                    for m in kls:
                        if m.value[i] == k:
                            return m

                setattr(cls, from_func, classmethod(mapfrom))

        return cls

    return inner
