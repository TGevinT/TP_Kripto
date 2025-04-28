from utils import read_key_file, bytes_to_int, int_to_bytes
from oaep import oaep_unpad

# untuk mendekripsi file yang dienkripsi menggunakan RSA dan OAEP padding
def rsa_decrypt_file(input_file: str, output_file: str, private_key_file: str):
    # untuk membaca nilai modulus (n) dan private exponent (d) dari file private key
    n, d = read_key_file(private_key_file)
    k = (n.bit_length() + 7) // 8

    # untuk membuka file input (ciphertext) untuk dibaca, dan file output (plaintext) untuk ditulis
    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        while True:
            chunk = fin.read(k) #baca satu chunk/block
            if not chunk:
                break
            if len(chunk) != k:
                raise ValueError("Invalid ciphertext block length")
            """
             Tahap konversi:
             1. chunk ke integer
             2. RSA dekripsi: m = c^d mod n
             3. Konversi hasil dekripsi kembali ke bytes
             4. Hilangkan OAEP padding
             5. Tulis hasil dekripsi ke file output
            """
            c_int = bytes_to_int(chunk)
            m_int = pow(c_int, d, n)
            em = int_to_bytes(m_int, k)
            message = oaep_unpad(em, k)
            fout.write(message)