from cryptography.fernet import Fernet
import base64
import os
from pathlib import Path

class ConfigEncryption:
    def __init__(self, key_file: str = ".config.key"):
        self.key_file = Path(key_file)
        self.key = self._load_or_generate_key()
        self.fernet = Fernet(self.key)

    def _load_or_generate_key(self) -> bytes:
        if self.key_file.exists():
            return self.key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            return key

    def encrypt_file(self, input_file: str, output_file: str):
        """Encripta un archivo de configuración"""
        with open(input_file, 'rb') as f:
            data = f.read()
        
        encrypted_data = self.fernet.encrypt(data)
        
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)

    def decrypt_file(self, input_file: str) -> str:
        """Desencripta un archivo de configuración"""
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = self.fernet.decrypt(encrypted_data)
        return decrypted_data.decode()