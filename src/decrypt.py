from utils import read_key_file, bytes_to_int, int_to_bytes
from oaep import oaep_unpad

def rsa_decrypt_file(input_file: str, output_file: str, private_key_file: str):
    n, d = read_key_file(private_key_file)
    k = (n.bit_length() + 7) // 8

    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        while True:
            chunk = fin.read(k)
            if not chunk:
                break
            if len(chunk) != k:
                raise ValueError("Invalid ciphertext block length")
            c_int = bytes_to_int(chunk)
            m_int = pow(c_int, d, n)
            em = int_to_bytes(m_int, k)
            message = oaep_unpad(em, k)
            fout.write(message)