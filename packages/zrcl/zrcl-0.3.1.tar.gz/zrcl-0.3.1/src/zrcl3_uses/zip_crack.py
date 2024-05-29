import typing
import py7zr


def attempted_check(password: str) -> bool:
    global _attempted
    if "_attempted" not in globals():
        import marisa_trie

        _attempted = marisa_trie.Trie()

    res = password in _attempted
    _attempted.add(password)
    return res


def crack_password(
    path: str,
    passwordStream: typing.Generator[str, None, None],
    maxAttempts: int = 1000,
    dedup: typing.Callable[[str], bool] = attempted_check,
):
    for i, password in enumerate(passwordStream):
        if i > maxAttempts:
            break
        if dedup(password):
            continue
        try:
            # Attempt to open the archive with the current password
            with py7zr.SevenZipFile(path, mode="r", password=password) as archive:
                archive.files
                return password  # Password is correct if no exception was raised
        except py7zr.Bad7zFile:
            # Continue with the next password if the file is bad or wrong password
            pass
        except Exception as e:
            # Raise exception if it's not related to LZMA errors
            if "_lzma.LZMAError" not in str(type(e)):
                raise e
