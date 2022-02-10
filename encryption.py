#!/usr/bin/python3

import base64
import sys
from operator import contains
from tkinter import E
from unittest import result
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def check_args(func):
    """Decorator for checking the number of args """

    def wrapper():
        if len(sys.argv) != 3:
            raise Exception("Wrong number of arguments")
        elif str(sys.argv[1]) != "-d" and sys.argv[1] != "-e":
            raise Exception("Crypto mode not chosen")
        return func()

    return wrapper

def log_genetor(func):
    """Log generator"""

    def wrapper():
        pass


class Crypto:
    """Encryption/decryption class"""

    def __init__(self) -> None:
        self.private_key = self.load_private_key()
        self.public_key = self.load_public_key()

    def load_private_key(self) -> 'cryptography.hazmat.backends.openssl.rsa._RSAPrivateKey':
        """Loads the private key"""

        with open("private_noshare.pem", "rb") as key_file:#open private key file and load it to a var
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None, backend=default_backend()
            )#serialize it and load up the key
            return private_key

    def load_public_key(self) -> 'cryptography.hazmat.backends.openssl.rsa._RSAPublicKey':
        """Loads the public key"""

        with open("public_shared.pem", "rb") as key_file:#open public key file and load it to a var
            public_key = serialization.load_pem_public_key(
                key_file.read(), backend=default_backend()
            )#serialize it and load up the key
            return public_key

    def encrypt(self, string_to_encrypt: str) -> str:
        """Encrypts a string. RSA with SHA256 padding"""

        to_encrypt = (
            bytes(string_to_encrypt, encoding="utf8")#convert to byte if no already in the format
            if not isinstance(string_to_encrypt, bytes)
            else string_to_encrypt
        )
        encrypted = self.public_key.encrypt(
            to_encrypt,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),#added SHA256 hash for padding
        )
        return str(base64.b64encode(encrypted))

    def decrypt(self, string_to_decrypt: str) -> str:
        """Decrypts a string. RSA with SHA256 padding"""
        
        try:
            to_decrypt = base64.b64decode(string_to_decrypt + "==")#decode base64 and leave the byte
        except Exception as e:
            print("String must be encoded")
            print(e)

        original_message = self.private_key.decrypt(
            to_decrypt,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),#decrypted RSA with SHA256 padding
        )
        return original_message.decode("utf-8").rstrip()


@check_args
def main():
    """Main method initializing objects and setting modes"""

    crypto = Crypto()
    if sys.argv[1] == "-d":
        print(crypto.decrypt(sys.argv[2]))
    else:
        print(crypto.encrypt(sys.argv[2]))


if __name__ == "__main__":
    main()
