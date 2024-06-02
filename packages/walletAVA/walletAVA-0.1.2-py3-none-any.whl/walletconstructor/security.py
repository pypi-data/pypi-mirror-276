from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from pathlib import Path
from web3 import Account 
from typing import Optional, Union
import os

class GenerateKey:
    def __init__(self, password: bytes) -> None:
        """
        Class to generate a new private key
        """
        self.__pwd = password
        self.__newprivatekey = self.__newkey()

    def __newkey(self) -> ec.EllipticCurvePrivateKey:
        """
        Generate a new EC private key using the SECP256R1 curve.
        """
        try:
            private_key = ec.generate_private_key(ec.SECP256R1())
            return private_key
        except Exception as e:
            raise RuntimeError("Failed to generate a new private key") from e

    def format_hex(self) -> str:
        """
        Format the private key to a hexadecimal string.
        """
        private_format = self.__newprivatekey.private_numbers().private_value.to_bytes(32, 'big').hex()
        return private_format

    @property
    def newkey(self) -> ec.EllipticCurvePrivateKey:
        """Generate a new private key"""
        return self.__newprivatekey

class LoadPrivateKey:
    @staticmethod
    def load_key(private_key: Optional[str] = None, password: Optional[str] = None) -> str:
        """
        Load or generate a private key.
        
        :param private_key: An existing private key in hex format (optional).
        :param password: Password to generate a new private key (optional).
        :return: Private key in hex format.
        :raises: Exception if no valid parameters are provided.
        """
        if private_key:
            return private_key
        elif private_key is None and password:
            new_private_key = GenerateKey(password.encode('utf-8'))
            return new_private_key.format_hex()
        else:
            raise ValueError("No valid parameters provided")

class Security:
    def __init__(self, private_key: Optional[str] = None, password: Optional[str] = None) -> None:
        """
        Security class to manage private key and account.

        :param private_key: An existing private key in hex format (optional).
        :param password: Password to generate a new private key (optional).
        """
        self.__private_key = LoadPrivateKey.load_key(private_key, password)
        self.__account = None
        self.__connect_profile()

    def __connect_profile(self) -> None:
        """
        Connect the profile using the private key.
        """
        try:
            self.__account = Account.from_key(self.__private_key)
        except Exception as e:
            raise RuntimeError("Failed to create an account from the private key") from e

    def save(self, path: Optional[Union[str, Path]] = None) -> Path:
        """
        Save the private key to a file.

        :param path: Path to save the private key (optional).
        :return: The path where the private key was saved.
        :raises: Exception if saving fails.
        """
        try:
            if path:
                with open(path, 'w') as f:
                    f.write(self.private_key)
                return Path(path)
            else:
                current_path = Path(os.getcwd())
                i = 0
                while True:
                    file = current_path / f'.unknown({i})'
                    if not file.exists():
                        with open(file, 'w') as f:
                            f.write(self.private_key)
                        return file
                    i += 1
        except Exception as e:
            raise IOError("Failed to save the private key to a file") from e

    @property
    def account(self):
        return self.__account

    @property
    def addr_ethereum(self):
        return self.account.address

    @property
    def private_key(self):
        return self.__private_key

    @property
    def sign_transaction(self):
        return self.account.sign_transaction
