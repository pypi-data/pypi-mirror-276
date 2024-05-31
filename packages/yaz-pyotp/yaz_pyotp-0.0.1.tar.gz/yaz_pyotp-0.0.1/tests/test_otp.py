# tests/test_otp.py

from src.yaz_pyotp.core.otp import LoginConfirmation, TwoFASetup, PasswordReset, AccountConfirmation
from src.yaz_pyotp.core.hasher import Hasher
from unittest.mock import Mock

def test_login_confirmation_creation():
    otp = LoginConfirmation()
    assert otp.length == 6
    assert otp.expires_in == 3
    assert otp.kind == "login"
    assert otp.template.startswith("Your one-time verification code to confirm your login")

def test_two_fa_setup_creation():
    otp = TwoFASetup()
    assert otp.length == 6
    assert otp.expires_in == 3
    assert otp.kind == "2fa_setup"
    assert otp.template.startswith("Your one-time verification code to set up 2FA")

def test_password_reset_creation():
    otp = PasswordReset()
    assert otp.length == 6
    assert otp.expires_in == 3
    assert otp.kind == "password_reset"
    assert otp.template.startswith("Your one-time verification code to reset your password")

def test_account_confirmation_creation():
    otp = AccountConfirmation()
    assert otp.length == 6
    assert otp.expires_in == 3
    assert otp.kind == "account_confirmation"
    assert otp.template.startswith("Your one-time verification code to confirm your account")

def test_create_otp(mock_create):
    otp = LoginConfirmation()
    is_created, code = otp.createOTP(mock_create)
    assert is_created
    assert len(code) == otp.length

def test_update_otp(mock_create, mock_get, mock_delete):
    otp = TwoFASetup()
    is_created, code = otp.updateOTP(mock_create, mock_get, mock_delete)
    assert is_created
    assert len(code) == otp.length

def test_verify_otp(mock_get, mock_delete):
    otp = PasswordReset()
    Hasher.hashCode = Mock(return_value="hashed_code")
    Hasher.compareHash = Mock(return_value=True)
    is_verified = otp.verifyOTP("normal_otp", mock_get, mock_delete)
    assert is_verified

def test_get_message_body():
    otp = AccountConfirmation()
    code = "123456"
    body = otp.getMessageBody(code)
    expected_body = otp.template.format(code=code, expires_in=otp.expires_in)
    assert body == expected_body
