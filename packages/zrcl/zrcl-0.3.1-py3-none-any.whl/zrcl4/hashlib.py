import hashlib
import io
from typing import overload
import os
import typing


@overload
def hash_file(file: str, algorithm="sha256", chunk_size=4096): ...
@overload
def hash_file(file: io.IOBase, algorithm="sha256", chunk_size=4096): ...


def hash_file(file, algorithm="sha256", chunk_size=4096):
    """Hash a file with the specified algorithm and chunk size."""
    fileIo = file if isinstance(file, io.IOBase) else io.open(file, "rb")
    hash_algo = hashlib.new(algorithm)
    chunk = fileIo.read(chunk_size)
    while chunk:
        hash_algo.update(chunk)
        chunk = fileIo.read(chunk_size)
    if file is not fileIo:
        fileIo.close()
    return hash_algo.hexdigest()


def hash_bytes(data, algorithm="sha256"):
    """Hash bytes with the specified algorithm."""
    return hashlib.new(algorithm, data).hexdigest()


def hash_folder(
    path: str,
    allowed_extensions: typing.List[str] = None,
    algorithm="sha256",
    chunk_size=4096,
):
    """Hash all files in a folder with the specified algorithm and return a dictionary of file hashes."""
    folder_hashes = {}
    collective_hash = hashlib.new(algorithm)
    for root, _, files in os.walk(path):
        for file in files:
            if allowed_extensions and not file.lower().endswith(
                tuple(allowed_extensions)
            ):
                continue
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path, algorithm, chunk_size)
            collective_hash.update(file_hash.encode("utf-8"))
            folder_hashes[file_path] = file_hash
    return folder_hashes, collective_hash.hexdigest()
