from collections.abc import Callable
import os
import typing
from zrcl4.hashlib import hash_file


# ANCHOR loading files
def get_serialize_data(path: str):
    if path.endswith(".json"):
        import json

        with open(path, "r") as f:
            return json.load(f)
    elif path.endswith(".yaml"):
        import yaml

        with open(path, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    elif path.endswith(".toml"):
        import toml

        with open(path, "r") as f:
            return toml.load(f)
    elif path.endswith(".pickle"):
        import pickle

        with open(path, "rb") as f:
            return pickle.load(f)
    else:
        raise NotImplementedError


class FilePropertyMeta:
    types = typing.Literal["mdate", "sha256", "size", "adate"]
    mapping: typing.Dict[types, typing.Callable[[str], typing.Any]] = {
        "mdate": lambda path: os.path.getmtime(path),
        "sha256": lambda path: hash_file(path),
        "size": lambda path: os.path.getsize(path),
        "adate": lambda path: os.path.getatime(path),
    }

    loadMethod: typing.Dict[str, typing.Callable[[str], typing.Any]] = {
        ".json": get_serialize_data,
        ".yaml": get_serialize_data,
        ".toml": get_serialize_data,
        ".pickle": get_serialize_data,
    }

    defaultLoad = lambda path: open(path, "r").read()  # noqa

    callBackHooks: typing.Dict[str, typing.Callable] = {}

    @staticmethod
    def registerCallbackHook(*hooks: str, callback: Callable = None):
        if callback is None and callable(hooks[-1]):
            callback = hooks[-1]
            hooks = hooks[:-1]

        for hook in hooks:
            FilePropertyMeta.callBackHooks[hook] = callback


class FileProperty:
    _properties: dict = {}
    _cachedContent: dict = {}

    def __init__(
        self,
        path: property | str,
        watching: typing.List[
            typing.Union[typing.List[FilePropertyMeta.types], FilePropertyMeta.types]
        ] = ["size", ["mdate", "sha256"]],
        customLoad: typing.Callable[[str], typing.Any] = None,
        customWatch: typing.Callable[[str], typing.Any] = None,
        fileCreate: typing.Callable[[str], typing.Any] = lambda path: open(
            path, "w"
        ).close(),
        callbacks: typing.List[typing.Union[str, typing.Callable]] = [],
    ):
        self.watching = watching
        self.path = path
        if fileCreate and not os.path.exists(path):
            fileCreate(path)

        self.customLoad = customLoad
        self.customWatch = customWatch
        self.callbacks = callbacks

    def _needToRefetch(
        self,
        watch: typing.Union[
            typing.List[FilePropertyMeta.types], FilePropertyMeta.types
        ],
        record: dict,
    ):
        """
        if is list, consider the whole watch true if any of it is true
        """
        if isinstance(watch, list):
            for w in watch:
                res = self._needToRefetch(w, record)
                if not res:
                    continue
                return True

            return False
        else:
            if watch not in record:
                oldval = None
            else:
                oldval = record[watch]

            if watch == "custom" and self.customWatch is None:
                raise RuntimeError("No custom watch function provided")

            elif watch == "custom" and self.customWatch is not None:
                newcheck = self.customWatch(self.path)
            else:
                newcheck = FilePropertyMeta.mapping[watch](self.path)

            if newcheck == oldval:
                return False
            else:
                record[watch] = newcheck
                return True

    def __get__(self, instance, owner):
        if isinstance(self.path, property):
            self.path = self.path.fget(instance)  # type: ignore

        if not os.path.exists(self.path):
            return None

        if self.path not in self._properties:
            self._properties[self.path] = {}

        recorded = self._properties[self.path]

        if not self._needToRefetch(self.watching, recorded):
            return self._cachedContent[self.path]

        if self.customLoad is not None:
            self._cachedContent[self.path] = self.customLoad(self.path)
        else:
            loadMethod = FilePropertyMeta.loadMethod.get(
                os.path.splitext(self.path)[1], FilePropertyMeta.defaultLoad
            )
            self._cachedContent[self.path] = loadMethod(self.path)

        for callback in self.callbacks:
            if isinstance(callback, str):
                callback = FilePropertyMeta.callBackHooks[callback]
            callback(
                self.path, self._cachedContent[self.path], self._properties[self.path]
            )

        return self._cachedContent[self.path]


# ANCHOR
def startApp(path: str):
    import zrcl4.subprocess as subprocess

    subprocess.exec_command(path)
