import hashlib
import socket
import random


def encrypt(object):
    sha_signature = \
        hashlib.sha256(str(object).encode()).hexdigest()
    return sha_signature


def includes(array: [], elements: []) -> bool:
    for e in elements:
        if not e in array:
            return False
    return True


def load_entrypoints(entry_name: str):
    # search in entry points
    import sys
    if sys.version_info < (3, 8):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    entrypoints = entry_points()
    if not entry_name in entrypoints.keys():
        return None
    return entrypoints[entry_name]


def find_open_ports() -> int:
    res = 0
    while res == 0:
        port = random.randint(10000, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            res = sock.connect_ex(('localhost', port))
            if res != 0:
                return port
