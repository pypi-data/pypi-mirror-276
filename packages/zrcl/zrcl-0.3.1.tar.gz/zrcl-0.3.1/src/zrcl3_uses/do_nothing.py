class Nothing:
    def __getattribute__(self, __name: str):
        if __name.startswith("__"):
            return object.__getattribute__(self, __name)

        return self

    def __call__(self, *args, **kwds):
        return self


NothingInstance = Nothing()
