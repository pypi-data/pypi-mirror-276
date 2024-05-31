import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .config import DEFAULT_ITERATIONS
from typing import Union

def generate_encryption_key(password: bytes, salt: bytes, iterations: int) -> bytes:
  """Generate encryption key from password, salt, and number of iterations."""
  kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
  return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt_message(msg: Union[str, bytes], password: str, iterations: int = DEFAULT_ITERATIONS) -> bytes:
    """Encrypts a message using a password."""
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    salt = secrets.token_bytes(32)
    key = generate_encryption_key(password.encode('utf-8'), salt, iterations)
    encrypted_msg = Fernet(key).encrypt(msg)
    return base64.urlsafe_b64encode(salt + iterations.to_bytes(4, 'big') + encrypted_msg)


def decrypt_message(encrypted_data: bytes, password: str) -> str:
    """Decrypts a message using a password."""
    decoded_data = base64.urlsafe_b64decode(encrypted_data)
    salt = decoded_data[:32]
    iterations = int.from_bytes(decoded_data[32:36], 'big')
    encrypted_msg = decoded_data[36:]
    key = generate_encryption_key(password.encode('utf-8'), salt, iterations)
    try:
        decrypted_msg = Fernet(key).decrypt(encrypted_msg).decode('utf-8')
        return decrypted_msg
    except:
        return None