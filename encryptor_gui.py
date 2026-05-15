import tkinter as tk
from tkinter import filedialog, messagebox
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit (32-byte) key from the given password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())

def encrypt_file_aes256(filepath, password):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        # Generate a random 16-byte salt and 12-byte nonce (IV)
        salt = os.urandom(16)
        nonce = os.urandom(12)
        
        # Derive 256-bit key
        key = derive_key(password, salt)
        
        # Encrypt data using AES-GCM
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, data, None)
        
        # Save salt + nonce + ciphertext to the new file
        enc_filepath = filepath + ".enc"
        with open(enc_filepath, 'wb') as f:
            f.write(salt + nonce + ciphertext)
            
        return True, enc_filepath
    except Exception as e:
        return False, str(e)

def decrypt_file_aes256(filepath, password):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()

        # Extract salt (16), nonce (12), and ciphertext
        salt = content[:16]
        nonce = content[16:28]
        ciphertext = content[28:]
        
        # Derive key
        key = derive_key(password, salt)
        
        # Decrypt data using AES-GCM
        aesgcm = AESGCM(key)
        data = aesgcm.decrypt(nonce, ciphertext, None)
        
        # Save decrypted data
        if filepath.endswith(".enc"):
            dec_filepath = filepath[:-4]
        else:
            dec_filepath = filepath + ".dec"
            
        with open(dec_filepath, 'wb') as f:
            f.write(data)
            
        return True, dec_filepath
    except Exception as e:
        return False, str(e)

class EncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced File Encryptor (AES-256)")
        self.root.geometry("450x250")
        self.root.resizable(False, False)
        
        self.filepath = None
        
        # UI Elements
        tk.Label(root, text="Select File:").grid(row=0, column=0, padx=10, pady=20, sticky="w")
        
        self.file_label = tk.Label(root, text="No file selected...", fg="grey", width=30, anchor="w")
        self.file_label.grid(row=0, column=1, padx=10, pady=20)
        
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10, pady=20)
        
        tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky="w")
        
        self.encrypt_btn = tk.Button(root, text="Encrypt File", command=self.encrypt, bg="#ff4d4d", fg="white", width=15)
        self.encrypt_btn.grid(row=2, column=0, columnspan=2, pady=30)
        
        self.decrypt_btn = tk.Button(root, text="Decrypt File", command=self.decrypt, bg="#4CAF50", fg="white", width=15)
        self.decrypt_btn.grid(row=2, column=1, columnspan=2, pady=30)

    def browse_file(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath:
            filename = os.path.basename(self.filepath)
            # Truncate if too long
            if len(filename) > 25:
                filename = filename[:22] + "..."
            self.file_label.config(text=filename, fg="black")
            
    def encrypt(self):
        if not self.filepath:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        pwd = self.password_entry.get()
        if not pwd:
            messagebox.showwarning("Warning", "Please enter a password!")
            return
            
        success, result = encrypt_file_aes256(self.filepath, pwd)
        if success:
            messagebox.showinfo("Success", f"File encrypted successfully!\nSaved as: {os.path.basename(result)}")
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Encryption failed:\n{result}")

    def decrypt(self):
        if not self.filepath:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        pwd = self.password_entry.get()
        if not pwd:
            messagebox.showwarning("Warning", "Please enter a password!")
            return
            
        success, result = decrypt_file_aes256(self.filepath, pwd)
        if success:
            messagebox.showinfo("Success", f"File decrypted successfully!\nSaved as: {os.path.basename(result)}")
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Decryption failed!\nIncorrect password or corrupted file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptorApp(root)
    root.mainloop()
