import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
import os
from rsa import generate_rsa_keypair
from encrypt import rsa_encrypt_file
from decrypt import rsa_decrypt_file

class RSAOAEPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA-OAEP")
        self.root.geometry("400x400")

        self.public_key_file = "keys/public.txt"
        self.private_key_file = "keys/private.txt"

        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="RSA-OAEP", font=("Helvetica", 18, "bold")).pack(pady=10)

        ttk.Button(main_frame, text="Generate RSA Key Pair", width=30, bootstyle="success", command=self.generate_keys).pack(pady=10, anchor='center')
        ttk.Button(main_frame, text="Encrypt File", width=30, bootstyle="primary", command=self.encrypt_file).pack(pady=5, anchor='center')
        ttk.Button(main_frame, text="Decrypt File", width=30, bootstyle="info", command=self.decrypt_file).pack(pady=5, anchor='center')

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

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = RSAOAEPApp(root)
    root.mainloop()
