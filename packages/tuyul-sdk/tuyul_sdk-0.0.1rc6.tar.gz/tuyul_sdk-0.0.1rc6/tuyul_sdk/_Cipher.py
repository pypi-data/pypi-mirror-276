import base64
import time
from typing import Dict, Literal, Union
import base58
from hexbytes import HexBytes
from Cryptodome.Hash import SHA256, MD5, SHA1
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Cipher import AES as aes
from Cryptodome.Random import get_random_bytes
import jwt

class Salt:

    @classmethod
    def create(cls):
        return cls(get_random_bytes(8))
    def __init__(self, keys: bytes) -> None:
        self.__k__ = keys
    def __str__(self) -> str:
        return str(self.__k__)
    def __repr__(self) -> str:
        return str(self.__k__)
    def __bytes__(self):
        return self.__k__    

class Password:

    @staticmethod
    def __check_password__(Password: Union[str, bytes]):
        if isinstance(Password, str):
            return Password.encode('utf-8')
        elif isinstance(Password, bytes):
            return Password
        else:
            raise TypeError('Password must be a string or bytes')

    @staticmethod
    def __check_salt__(salt: Union[Salt, bytes, str]):
        if isinstance(salt, Salt):
            return bytes(salt)
        elif isinstance(salt, bytes):
            return salt
        elif isinstance(salt, str):
            return salt.encode('utf-8')
        else:
            raise TypeError('Salt must be a string or bytes')
    
    @classmethod
    def create(cls, Password: Union[str, bytes], salt: Union[Salt, bytes, str], count: int = 1, dkLen: int = 16, hmac_hash_module = SHA1, addTextFront: str = '', addTextBack: str = ''):
        return cls(addTextFront + PBKDF2(cls.__check_password__(Password), cls.__check_salt__(salt), dkLen, count, hmac_hash_module=hmac_hash_module).hex() + addTextBack)
    def __init__(self, password: str) -> None:
        self.PBKDF2 = password
    def __str__(self) -> str:
        return self.PBKDF2
    def __repr__(self) -> str:
        return self.PBKDF2
    def __bytes__(self):
        return self.PBKDF2.encode('utf-8')

class Encrypt:

    def __init__(self, Result: Dict[str, any]) -> None:
        self.Bytes: bytes   = Result.get('Encrypt').get('Bytes')
        self.Base64: str    = Result.get('Encrypt').get('Base64')
        self.Base58: str    = Result.get('Encrypt').get('Base58')
        self.Hex: str       = Result.get('Encrypt').get('Hex')
        self.IV: str        = Result.get('IV')
        self.KEY: str       = Result.get('KEY')
        self.Salt: Union[str, None]= Result.get('Salt')
    def __str__(self) -> str:
        return str(self.__dict__)
    def __repr__(self) -> str:
        return str(self.__dict__)

class Decrypt:

    def __init__(self, Result: Dict[str, any]) -> None:
        self.Bytes: bytes   = Result.get('Decrypt').get('CipherBytes')
        self.String: str    = Result.get('Decrypt').get('CipherString')
        self.IV: str        = Result.get('IV')
        self.KEY: str       = Result.get('KEY')
    def __str__(self) -> str:
        return str(self.__dict__)
    def __repr__(self) -> str:
        return str(self.__dict__)
    
class AES:
    
    @staticmethod
    def pad(PlainText: bytes, size: int):
        return PlainText + (size - len(PlainText) % size) * bytes(chr(0), encoding='utf-8')
        
    @staticmethod
    def unpad(PlainText: bytes):
        return ''.join([chr(s) if int(s) != 0 else '' for s in PlainText]).encode()

    @staticmethod
    def __check_password__(password: Union[Password, str, bytes]):
        if isinstance(password, Password):
            return bytes(password)
        elif isinstance(password, str):
            return password.encode('utf-8')
        elif isinstance(password, bytes):
            return password
        else:
            raise TypeError('Password must be a string or bytes')
    
    @staticmethod
    def __check_salt__(salt: Union[Salt, bytes, str]):
        if isinstance(salt, Salt):
            return bytes(salt)
        elif isinstance(salt, bytes):
            return salt
        elif isinstance(salt, str):
            return salt.encode('utf-8')
        else:
            raise TypeError('Salt must be a string or bytes')

    @classmethod
    def key_iv(cls, salt: Union[Salt, bytes, str], Password: Password):
        derived = b""
        while len(derived) < 48:
            hasher = MD5.new()
            hasher.update(derived[-16:] + cls.__check_password__(Password) + cls.__check_salt__(salt))
            derived += hasher.digest()
        KEY = derived[0:32]
        IV  = derived[32:48]
        return KEY, IV
    
    @staticmethod
    def __to_bytes__(data: Union[str, bytes, Password, Salt]):
        if isinstance(data, str):
            return data.encode('utf-8')
        elif isinstance(data, bytes):
            return data
        elif isinstance(data, Password):
            return bytes(data)
        elif isinstance(data, Salt):
            return bytes(data)
        else:
            raise TypeError('Data must be a string or bytes')
    
    @classmethod
    def Encrypt(cls, PlainText: Union[str, bytes], KEY: Union[str, bytes], IV: Union[str, bytes] = None, Salt: Union[str, bytes, Salt] = None, MODE: Literal[2] = aes.MODE_CBC):

        PlainText   = cls.__to_bytes__(PlainText)
        KEY         = cls.__to_bytes__(KEY)
        IV          = cls.__to_bytes__(IV) if IV is not None else cls.__to_bytes__(get_random_bytes(16))

        cipher = aes.new(KEY, MODE, IV).encrypt(cls.pad(PlainText, aes.block_size))
        if Salt is not None:
            Salt            = cls.__to_bytes__(Salt)
            Bytes: bytes    = b'Salted__' + Salt + cipher
        else:
            Bytes: bytes   = cipher        
        return Encrypt(dict(
            Encrypt = dict(
                Bytes   = Bytes,
                Base64  = base64.b64encode(Bytes).decode('utf-8'),
                Base58  = base58.b58encode(Bytes).decode('utf-8'),
                Hex     = Bytes.hex()
            ),
            IV      = IV.hex(),
            KEY     = KEY.hex(),
            Salt    = Salt.hex() if Salt is not None else None
        ))
    
    @staticmethod
    def to_decode(PlainText: Union[str, bytes]):
        if isinstance(PlainText, str):
            try:
                decode = base64.b64decode(PlainText)
                if PlainText == base64.b64encode(decode).decode():
                    return decode
            except: pass
            try:
                decode = base58.b58decode(PlainText)
                if PlainText == base58.b58encode(decode).decode():
                    return decode
            except: pass
            try:
                return HexBytes(PlainText)
            except: pass
        elif isinstance(PlainText, (bytes, HexBytes, bytearray)):
            return PlainText
        else:
            raise TypeError('Data must be a string or bytes')        

    @classmethod
    def Decrypt(cls, PlainText: Union[str, bytes], KEY: Union[str, bytes], IV: Union[str, bytes], MODE: Literal[2] = aes.MODE_CBC):
        PlainText   = cls.__to_bytes__(PlainText)
        KEY         = cls.__to_bytes__(KEY)
        IV          = cls.__to_bytes__(IV)

        cipher = aes.new(KEY, MODE, IV).decrypt(PlainText)
        CipherBytes: bytes = cls.unpad(cipher)
        return Decrypt(dict(
            Decrypt = dict(
                CipherBytes     = CipherBytes,
                CipherString    = CipherBytes.decode()
            ),
            IV      = IV.hex(),
            KEY     = KEY.hex()
        ))

    @classmethod
    def create_encrypt_with_password(cls, PlainText: Union[str, bytes], password: Union[str, bytes]):
        salt        = Salt.create()
        password    = Password.create(password, salt)
        KEY, IV     = cls.key_iv(salt, password)
        return cls.Encrypt(PlainText, KEY, IV, salt)
    
    @classmethod
    def create_encrypt_with_key_iv(cls, PlainText: Union[str, bytes], KEY: Union[str, bytes], IV: Union[str, bytes]):
        return cls.Encrypt(PlainText, KEY, IV)
    
    @classmethod
    def create_decrypt_with_password(cls, PlainText: Union[str, bytes], password: Union[str, bytes]):
        to_decode   = cls.to_decode(PlainText)
        KEY, IV     = cls.key_iv(to_decode[8:16], Password.create(password, to_decode[8:16]))
        return cls.Decrypt(to_decode[16:], KEY, IV)
    
    @classmethod
    def create_decrypt_with_key_iv(cls, PlainText: Union[str, bytes], KEY: Union[str, bytes], IV: Union[str, bytes]):
        return cls.Decrypt(PlainText, KEY, IV)

