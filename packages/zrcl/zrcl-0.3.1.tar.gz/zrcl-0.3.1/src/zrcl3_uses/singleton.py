class SingletonClssed(type):
    _cls = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._cls:
            cls._cls[cls] = super(SingletonClssed, cls).__call__(*args, **kwargs)
        return cls._cls[cls]


class SingletonOne(type):
    _ins = None

    def __call__(cls, *args, **kwargs):
        if cls._ins is None:
            cls._ins = super(SingletonOne, cls).__call__(*args, **kwargs)
        return cls._ins
