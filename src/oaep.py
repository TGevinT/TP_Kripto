from sha256 import sha256
from utils import secure_random_bytes

def mgf1(seed: bytes, length: int) -> bytes:
    output = b''
    counter = 0
    while len(output) < length:
        output += sha256(seed + counter.to_bytes(4, 'big'))
        counter += 1
    return output[:length]

def oaep_pad(message: bytes, k: int) -> bytes:
    h_len = 32
    l_hash = sha256(b'')
    ps = b'\x00' * (k - len(message) - 2 * h_len - 2)
    db = l_hash + ps + b'\x01' + message
    seed = secure_random_bytes(h_len)
    db_mask = mgf1(seed, k - h_len - 1)
    masked_db = bytes(x ^ y for x, y in zip(db, db_mask))
    seed_mask = mgf1(masked_db, h_len)
    masked_seed = bytes(x ^ y for x, y in zip(seed, seed_mask))
    return b'\x00' + masked_seed + masked_db

def oaep_unpad(em: bytes, k: int) -> bytes:
    h_len = 32
    y, masked_seed, masked_db = em[0], em[1:1+h_len], em[1+h_len:]
    if y != 0:
        raise ValueError("decryption error")
    seed_mask = mgf1(masked_db, h_len)
    seed = bytes(x ^ y for x, y in zip(masked_seed, seed_mask))
    db_mask = mgf1(seed, k - h_len - 1)
    db = bytes(x ^ y for x, y in zip(masked_db, db_mask))
    l_hash = sha256(b'')
    if db[:h_len] != l_hash:
        raise ValueError("decryption error")
    i = db.find(b'\x01', h_len)
    if i == -1:
        raise ValueError("decryption error")
    return db[i+1:]
