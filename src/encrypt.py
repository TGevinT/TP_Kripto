from utils import read_key_file, bytes_to_int, int_to_bytes
from oaep import oaep_pad

# untuk mengenkripsi file menggunakan RSA dan OAEP padding
def rsa_encrypt_file(input_file: str, output_file: str, public_key_file: str):
    # untuk baca nilai modulus (n) dan public exponent (e) dari file public key
    n, e = read_key_file(public_key_file)
    k = (n.bit_length() + 7) // 8
    h_len = 32
    max_block_size = k - 2 * h_len - 2

    # untuk buka file input (plaintext) untuk dibaca, dan file output (ciphertext) untuk ditulis
    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        while True:
            chunk = fin.read(max_block_size)
            if not chunk:
                break
            """
            Instruksi
            1. Tambahkan OAEP Padding
            2. Konversi Data ke Integer
            3. RSA enkripsi: c = m^e mod n
            4. Tulis ciphertext ke file output
            """
            padded = oaep_pad(chunk, k)
            m_int = bytes_to_int(padded)
            c_int = pow(m_int, e, n)
            fout.write(int_to_bytes(c_int, k))