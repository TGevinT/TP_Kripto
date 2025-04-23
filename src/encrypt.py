from utils import read_key_file, bytes_to_int, int_to_bytes
from oaep import oaep_pad

def rsa_encrypt_file(input_file: str, output_file: str, public_key_file: str):
    n, e = read_key_file(public_key_file)
    k = (n.bit_length() + 7) // 8
    h_len = 32
    max_block_size = k - 2 * h_len - 2

    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        while True:
            chunk = fin.read(max_block_size)
            if not chunk:
                break
            padded = oaep_pad(chunk, k)
            m_int = bytes_to_int(padded)
            c_int = pow(m_int, e, n)
            fout.write(int_to_bytes(c_int, k))