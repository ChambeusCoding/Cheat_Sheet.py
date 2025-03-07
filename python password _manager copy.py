import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

USER_PASSWORD_FILE = "user_password.txt"
ADMIN_PASSWORD_FILE = "admin_password.txt"
ENCYPTION_KEY = b"0123456789abcdef"

def encypt_password(password):
    padder = padding.PKCS7(128).padder() # Public Key Cryptography Standards #7
    padded_data = padder.update(password.encode()) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(os.urandom(16)), backend=defualt_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    return base64.b64encode(cipher.iv + encrypted).decode('utf-8')
    