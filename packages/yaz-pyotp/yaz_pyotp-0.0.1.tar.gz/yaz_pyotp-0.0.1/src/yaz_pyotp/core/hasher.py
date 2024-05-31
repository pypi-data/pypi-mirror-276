from ..settings import Settings
import hmac
import hashlib

def create_hmac(data:str, key:str) -> str:
        byte_key = key.encode('utf-8')
        message = data.encode('utf-8')
        return hmac.new(byte_key, message, hashlib.sha256).hexdigest()

def verify_hmac(data:str, hmac_to_verify:str, key:str) -> bool:
    return hmac.compare_digest(create_hmac(data,key), hmac_to_verify)

class Hasher:
    @staticmethod
    def getSecretKey():
        secret_key = getattr(Settings, "secret_key", None)
        if secret_key is None:
            raise ValueError("secret_key was configure in Otp Settings")
        return secret_key

    @staticmethod
    def hashCode(code:str):
        secret_key = Hasher.getSecretKey()
        return create_hmac(code, secret_key)

    @staticmethod
    def compareHash(hashed_code:str, new_code:str):
        secret_key = Hasher.getSecretKey()
        return verify_hmac(new_code, hashed_code, secret_key)
    

