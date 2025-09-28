from cryptography.fernet import Fernet
import os

# -----------------------------
# Use the key from your .env
# Example: SESSION_ENCRYPTION_KEY=MySuperSecretKey1234567890==
# -----------------------------
KEY = os.getenv("SESSION_ENCRYPTION_KEY=MySuperSecretKey1234567890==").encode()  
fernet = Fernet(KEY)

# -----------------------------
# Encrypt a session string
# -----------------------------
def encrypt_session(session_string):
    """
    Encrypts a user session string before saving to MongoDB
    """
    return fernet.encrypt(session_string.encode()).decode()

# -----------------------------
# Decrypt a session string
# -----------------------------
def decrypt_session(enc_string):
    """
    Decrypts a session string from MongoDB
    """
    return fernet.decrypt(enc_string.encode()).decode()
