import hashlib

def encrypt(object):
    sha_signature = \
        hashlib.sha256(str(object).encode()).hexdigest()
    return sha_signature

def includes(array: [], elements: []) -> bool:
    for e in elements:
        if not e in array:
            return False
    return True