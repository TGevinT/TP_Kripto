# src/main.py

from rsa import generate_keypair

def save_hex(file_path: str, *ints: int):
    """
    Simpan satu atau lebih bilangan ke file dalam heksadesimal,
    satu per baris (tanpa prefix 0x).
    """
    with open(file_path, "w") as f:
        for num in ints:
            hexstr = format(num, 'x')
            if len(hexstr) % 2:
                hexstr = '0' + hexstr
            f.write(hexstr + "\n")

def main():
    # sesuai slide: KU = (e, n), KR = (d, n)
    e, d, n = generate_keypair(2048)

    # simpan public key: first line e, second line n
    save_hex("public_key.txt", e, n)

    # simpan private key: first line d, second line n
    save_hex("private_key.txt", d, n)

    print("RSA key pair 2048-bit berhasil digenerate:")
    print("  • public_key.txt  ← (e, n)")
    print("  • private_key.txt ← (d, n)")

if __name__ == "__main__":
    main()
