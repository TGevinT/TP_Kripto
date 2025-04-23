import tkinter as tk
from tkinter import filedialog, messagebox
import os
from rsa import generate_rsa_keypair
from encrypt import rsa_encrypt_file
from decrypt import rsa_decrypt_file
import filecmp

class RSAOAEPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA-OAEP Encryption/Decryption")

        self.public_key_file = "keys/public.txt"
        self.private_key_file = "keys/private.txt"
        self.test_file_path = None
        self.encrypted_file_path = "test_cipher.bin"
        self.decrypted_file_path = "test_decrypted"

        tk.Button(root, text="Generate RSA Key Pair", command=self.generate_keys).pack(pady=5)
        tk.Button(root, text="Encrypt File", command=self.encrypt_file).pack(pady=5)
        tk.Button(root, text="Decrypt File", command=self.decrypt_file).pack(pady=5)
        tk.Button(root, text="Run File Integrity Test", command=self.test_integrity).pack(pady=5)

    def generate_keys(self):
        try:
            generate_rsa_keypair()
            messagebox.showinfo("Success", "RSA key pair generated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def encrypt_file(self):
        input_file = filedialog.askopenfilename(title="Select file to encrypt")
        if not input_file:
            return
        output_file = filedialog.asksaveasfilename(title="Save encrypted file as", defaultextension=".bin")
        if not output_file:
            return
        try:
            rsa_encrypt_file(input_file, output_file, self.public_key_file)
            messagebox.showinfo("Success", "File encrypted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt_file(self):
        input_file = filedialog.askopenfilename(title="Select file to decrypt")
        if not input_file:
            return
        output_file = filedialog.asksaveasfilename(title="Save decrypted file as")
        if not output_file:
            return
        try:
            rsa_decrypt_file(input_file, output_file, self.private_key_file)
            messagebox.showinfo("Success", "File decrypted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def test_integrity(self):
        self.test_file_path = filedialog.askopenfilename(title="Pilih file untuk pengujian integritas")
        if not self.test_file_path:
            return
        try:
            rsa_encrypt_file(self.test_file_path, self.encrypted_file_path, self.public_key_file)
            rsa_decrypt_file(self.encrypted_file_path, self.decrypted_file_path, self.private_key_file)
            if filecmp.cmp(self.test_file_path, self.decrypted_file_path, shallow=False):
                messagebox.showinfo("Test Result", "✅ File integrity verified after encryption and decryption.")
            else:
                messagebox.showerror("Test Result", "❌ File mismatch after decryption.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = RSAOAEPApp(root)
    root.mainloop()
