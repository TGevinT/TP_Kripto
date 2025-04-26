from utils import is_prime, modinv, write_key_file, secure_random_bits

# untuk menghasilkan bilangan prima besar dengan panjang bit tertentu
def generate_large_prime(bits=1024):
    while True:
        num = secure_random_bits(bits)
        num |= (1 << bits - 1) | 1  # set MSB and LSB to 1
        if is_prime(num):
            return num

# untuk menghasilkan pasangan kunci RSA (public dan private)
def generate_rsa_keypair():
    print("Generating 2048-bit RSA key pair...")
    # 2 bilangan prima p dan q
    p = generate_large_prime(1024)
    q = generate_large_prime(1024)
    while q == p:
        q = generate_large_prime(1024)

    """
    Info:
    1. n -> modulus
    2. phi -> Euler's totient function
    3. e -> Public exponent (nilai umum)
    4. d -> Private exponent (modular inverse dari e mod phi)
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
# Simpan kunci ke file
    write_key_file("keys/public.txt", n, e)
    write_key_file("keys/private.txt", n, d)

    print("Keys generated and saved to keys/ directory.")

if __name__ == "__main__":
    generate_rsa_keypair()