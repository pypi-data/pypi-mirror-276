import typing


def split_keys(key: str, delimiter: str = "/"):
    return key.split(delimiter)


def get_deep(obj: typing.Union[dict, list, set, tuple], *keys):
    curr = obj
    for key in keys:
        if isinstance(curr, dict):
            curr = curr.get(key)
        elif isinstance(curr, (list, set, tuple)):
            curr = curr[int(key)]
        else:
            curr = getattr(curr, key)

    return curr


def set_deep(obj: typing.Union[dict, list, set, tuple], *keys, value):
    curr = obj
    for key in keys[:-1]:
        if isinstance(curr, dict):
            curr = curr.get(key)
        elif isinstance(curr, (list, set, tuple)):
            curr = curr[int(key)]
        else:
            curr = getattr(curr, key)

    if isinstance(curr, dict):
        curr[keys[-1]] = value
    elif isinstance(curr, (list, set, tuple)):
        curr[int(keys[-1])] = value
    else:
        setattr(curr, keys[-1], value)


def del_deep(obj: typing.Union[dict, list, set, tuple], *keys):
    curr = obj
    for key in keys[:-1]:
        if isinstance(curr, dict):
            curr = curr.get(key)
        elif isinstance(curr, (list, set, tuple)):
            curr = curr[int(key)]
        else:
            curr = getattr(curr, key)

    if isinstance(curr, dict):
        del curr[keys[-1]]
    elif isinstance(curr, (list, set, tuple)):
        del curr[int(keys[-1])]
    else:
        delattr(curr, keys[-1])


def set_default_deep(
    obj: typing.Union[dict, list, set, tuple], *keys, value, fillpadding=False
):

    curr = obj
    for key in keys[:-1]:
        if isinstance(curr, dict):
            curr = curr.get(key)
        elif isinstance(curr, (list, set, tuple)):
            curr = curr[int(key)]
        else:
            curr = getattr(curr, key)

    if isinstance(curr, set):
        raise IndexError("set does not support default value")

    # check has attr
    if (
        (isinstance(curr, dict) and keys[-1] in curr)
        or (isinstance(curr, (list, set, tuple)) and int(keys[-1]) < len(curr))
        or (not isinstance(curr, (dict, list, set, tuple)) and hasattr(curr, keys[-1]))
    ):
        return

    if isinstance(curr, dict):
        curr[keys[-1]] = value
    elif isinstance(curr, (list, tuple)):
        if len(curr) + 1 < int(keys[-1]) and not fillpadding:
            raise IndexError

        while len(curr) < int(keys[-1]):
            curr.append(None)

        curr[int(keys[-1])] = value
    else:
        setattr(curr, keys[-1], value)
