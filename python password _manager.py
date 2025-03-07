import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

# Constants for file names and encryption key
USER_PASSWORD_FILE = "user_password.txt"
ADMIN_PASSWORD_FILE = "admin_password.txt"
ENCRYPTION_KEY = b"0123456789abcdef"  # 16-byte key for AES

# Encryption and Decryption Functions
def encrypt_password(password):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(os.urandom(16)), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(cipher.iv + encrypted).decode('utf-8')


def decrypt_password(encrypted_password):
    encrypted_data = base64.b64decode(encrypted_password)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted) + unpadder.finalize()

    return unpadded_data.decode()


# File handling functions
def read_user_password():
    try:
        with open(USER_PASSWORD_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def store_user_password(password):
    encrypted_password = encrypt_password(password)
    with open(USER_PASSWORD_FILE, 'w') as file:
        file.write(encrypted_password)


def read_admin_password():
    try:
        with open(ADMIN_PASSWORD_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def store_admin_password(password):
    encrypted_password = encrypt_password(password)
    with open(ADMIN_PASSWORD_FILE, 'w') as file:
        file.write(encrypted_password)


# Generate a random password (12 characters)
def generate_password():
    import random
    import string

    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(12))


# Verify password (check against stored password)
def verify_user_password(entered_password):
    stored_password = read_user_password()
    if stored_password is None:
        return False
    try:
        decrypted_password = decrypt_password(stored_password)
        return decrypted_password == entered_password
    except Exception:
        return False


def verify_admin_password(entered_password):
    stored_password = read_admin_password()
    if stored_password is None:
        return False
    try:
        decrypted_password = decrypt_password(stored_password)
        return decrypted_password == entered_password
    except Exception:
        return False


# GUI functions
class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("W.O.P.R Joshua")
        self.root.geometry("500x600")
        self.root.configure(bg="darkred")

        self.message_label = tk.Label(self.root, text="Opening Joshua...\nUser or Admin Mode.", font=("Segoe Print", 18), bg="darkred", fg="white")
        self.message_label.pack(pady=20)

        self.user_button = tk.Button(self.root, text="User", font=("Segoe Print", 18), command=self.handle_user_mode)
        self.user_button.pack(pady=10)

        self.admin_button = tk.Button(self.root, text="Admin", font=("Segoe Print", 18), command=self.handle_admin_mode)
        self.admin_button.pack(pady=10)

    def handle_user_mode(self):
        self.message_label.config(text="User Mode: Verify or Generate password.\n")

        user_password = read_user_password()
        if user_password is None:
            generated_password = generate_password()
            self.message_label.config(text=f"Generated Password: {generated_password}\n")
            store_user_password(generated_password)
        else:
            entered_password = simpledialog.askstring("Password", "Enter your password:")
            if verify_user_password(entered_password):
                self.message_label.config(text="Access granted... Accessing W.O.P.R")
            else:
                self.message_label.config(text="Incorrect password. Access denied.")

    def handle_admin_mode(self):
        self.message_label.config(text="Enter Admin to reset W.O.P.R.\n")

        admin_password = read_admin_password()
        if admin_password is None:
            entered_password = simpledialog.askstring("Set Admin Password", "Set Admin password:")
            store_admin_password(entered_password)
            self.message_label.config(text="Admin password set successfully.\n")

        entered_admin_password = simpledialog.askstring("Admin Password", "Enter Admin password:")
        if verify_admin_password(entered_admin_password):
            self.message_label.config(text="Admin access granted... Accessing W.O.P.R")
            self.message_label.config(text="Greetings Professor Falken... Shall we play a game?\n")
            self.reset_user_password()
        else:
            self.message_label.config(text="Incorrect admin password.")

    def reset_user_password(self):
        new_password = simpledialog.askstring("Play Thermonuclear War?", "Enter new user password:")
        store_user_password(new_password)
        self.message_label.config(text="A strange game. The winning move is not to play.")


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()