from utils import read_key_file, bytes_to_int, int_to_bytes
from oaep import oaep_unpad

def rsa_decrypt_file(input_file: str, output_file: str, private_key_file: str):
    n, d = read_key_file(private_key_file)
    with open(input_file, 'rb') as f:
        ciphertext = f.read()
    k = (n.bit_length() + 7) // 8
    c_int = bytes_to_int(ciphertext)
    m_int = pow(c_int, d, n)
    em = int_to_bytes(m_int, k)
    message = oaep_unpad(em, k)
    with open(output_file, 'wb') as f:
        f.write(message)