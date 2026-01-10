from cryptography.fernet import Fernet
from django.conf import settings
import json

def get_cipher_suite():
    key = settings.ENCRYPTION_KEY
    if not key:
        raise ValueError("ENCRYPTION_KEY not set in settings.")
    return Fernet(key)

def encrypt_data(data_dict):
    """
    Encrypts a dictionary into a fernet token string.
    """
    if not data_dict:
        return None
    
    cipher_suite = get_cipher_suite()
    json_str = json.dumps(data_dict)
    token = cipher_suite.encrypt(json_str.encode('utf-8'))
    return token.decode('utf-8')

def decrypt_data(token_str):
    """
    Decrypts a fernet token string back to a dictionary.
    """
    if not token_str:
        return {}
        
    try:
        cipher_suite = get_cipher_suite()
        json_bytes = cipher_suite.decrypt(token_str.encode('utf-8'))
        return json.loads(json_bytes.decode('utf-8'))
    except Exception as e:
        print(f"Decryption failed: {e}")
        return {}
