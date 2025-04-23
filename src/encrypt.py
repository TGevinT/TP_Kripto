from utils import read_key_file, bytes_to_int, int_to_bytes
from oaep import oaep_pad

def rsa_encrypt_file(input_file: str, output_file: str, public_key_file: str):
    n, e = read_key_file(public_key_file)
    with open(input_file, 'rb') as f:
        message = f.read()
    k = (n.bit_length() + 7) // 8
    padded = oaep_pad(message, k)
    m_int = bytes_to_int(padded)
    c_int = pow(m_int, e, n)
    with open(output_file, 'wb') as f:
        f.write(int_to_bytes(c_int, k))