# src/rsa.py

import secrets
import math

def is_prime(n: int, k: int = 40) -> bool:
    """Miller–Rabin probabilistic primality test."""
    if n < 2:
        return False
    # cek faktor kecil
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    # tulis n − 1 = d·2^s
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def trial(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # random in [2, n-2]
        if not trial(a):
            return False
    return True

def generate_prime(bits: int) -> int:
    """Buat bilangan prima acak dengan panjang bits."""
    while True:
        # set bit tertinggi & terendah -> ganjil dan tepat bits‐bit panjangnya
        p = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(p):
            return p

def extended_gcd(a: int, b: int):
    """
    +    Iterative Extended Euclidean Algorithm.
    +    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    # now a = gcd, and x0,y0 are the Bezout coefficients
    return a, x0, y0

def modinv(a: int, m: int) -> int:
    """Modular inverse a⁻¹ mod m."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Tidak ada invers modulo")
    return x % m

def choose_public_exponent(phi: int) -> int:
    """
    Pilih e secara random: 1 < e < phi, dan gcd(e,phi)=1
    """
    while True:
        e = secrets.randbelow(phi - 2) + 2  # di [2, phi-1]
        if math.gcd(e, phi) == 1:
            return e

def generate_keypair(key_size: int = 2048):
    """
    Generate RSA keypair sesuai slide:
      1) pilih p,q prime (p≠q) setengah panjang key_size
      2) n = p·q
      3) φ(n) = (p−1)(q−1)
      4) pilih e random: 1<e<φ, gcd(e,φ)=1
      5) hitung d = e⁻¹ mod φ(n)
      6) return (e, d, n)
    """
    half = key_size // 2
    p = generate_prime(half)
    q = generate_prime(half)
    while q == p:
        q = generate_prime(half)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = choose_public_exponent(phi)
    d = modinv(e, phi)

    return e, d, n
