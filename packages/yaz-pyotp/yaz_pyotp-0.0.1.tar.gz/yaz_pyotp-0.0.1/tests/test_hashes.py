from src.yaz_pyotp.core.hasher import create_hmac, Hasher, verify_hmac, Settings
# import pytest 
import hmac
import hashlib

def test_create_hmac():
    data = "test_data"
    key = "test_key"
    expected_hmac = hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()
    assert create_hmac(data, key) == expected_hmac

def test_verify_hmac():
    data = "test_data"
    key = "test_key"
    generated_hmac = create_hmac(data, key)
    assert verify_hmac(data, generated_hmac, key)
    assert not verify_hmac(data, "invalid_hmac", key)

def test_hashCode():
    code = "123456"
    expected_hmac = create_hmac(code, Settings.secret_key)
    assert Hasher.hashCode(code) == expected_hmac

def test_compareHash():
    code = "123456"
    hashed_code = Hasher.hashCode(code)
    assert Hasher.compareHash(hashed_code, code)
    assert not Hasher.compareHash(hashed_code, "654321")

# def test_missing_secret_key():
#     # Backup and remove the secret key
#     original_key = Hasher.secret_key
#     Hasher.secret_key = None
    
#     with pytest.raises(ValueError, match="secret_key must be configured in Otp Settings"):
#         Hasher.hashCode("123456")

#     with pytest.raises(ValueError, match="secret_key must be configured in Otp Settings"):
#         Hasher.compareHash("some_hashed_code", "123456")
    
#     # Restore the secret key
#     Hasher.secret_key = original_key
