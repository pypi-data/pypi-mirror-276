from typing import get_overloads, get_type_hints
import inspect


def get_overload_signatures(func):
    overloads = get_overloads(func)
    for overloadFunc in overloads:
        yield inspect.signature(overloadFunc)


def bind_overload(overloadFunc, *args, **kwargs):
    for sig in get_overload_signatures(overloadFunc):
        try:
            return sig.bind(*args, **kwargs).arguments
        except TypeError:
            pass


def is_valid_typeddict(instance, typeddict: type) -> bool:
    required_keys = {
        k for k, v in get_type_hints(typeddict).items() if not isinstance(v, type(None))
    }
    optional_keys = {
        k for k, v in get_type_hints(typeddict).items() if isinstance(v, type(None))
    }

    # Check for required keys and correct types
    if not all(
        k in instance and isinstance(instance[k], get_type_hints(typeddict)[k])
        for k in required_keys
    ):
        return False

    # Check for optional keys and correct types if present
    if not all(
        isinstance(instance[k], get_type_hints(typeddict)[k])
        for k in optional_keys
        if k in instance
    ):
        return False

    # Optionally, ensure no extra keys are present
    all_keys = required_keys.union(optional_keys)
    if not all(k in all_keys for k in instance.keys()):
        return False

    return True


class ClassProperty(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self
