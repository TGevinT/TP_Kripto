from utils import is_prime, modinv, write_key_file, secure_random_bits

def generate_large_prime(bits=1024):
    while True:
        num = secure_random_bits(bits)
        num |= (1 << bits - 1) | 1  # set MSB and LSB to 1
        if is_prime(num):
            return num

def generate_rsa_keypair():
    print("Generating 2048-bit RSA key pair...")

    p = generate_large_prime(1024)
    q = generate_large_prime(1024)
    while q == p:
        q = generate_large_prime(1024)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)

    write_key_file("keys/public.txt", n, e)
    write_key_file("keys/private.txt", n, d)

    print("Keys generated and saved to keys/ directory.")

if __name__ == "__main__":
    generate_rsa_keypair()