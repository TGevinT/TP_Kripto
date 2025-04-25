import os
import secrets

def read_key_file(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().strip(), 16)
        exp = int(f.readline().strip(), 16)
    return n, exp

def write_key_file(filename, n, exp):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(hex(n)[2:] + '\n')
        f.write(hex(exp)[2:] + '\n')

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')

def int_to_bytes(i, length):
    return i.to_bytes(length, byteorder='big')

def secure_random_bits(bits):
    return secrets.randbits(bits)

def secure_random_bytes(length):
    return secrets.token_bytes(length)

def is_prime(n, k=5):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def egcd(a, b):
    if a == 0: return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    return x % m
