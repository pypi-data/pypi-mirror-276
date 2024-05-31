import pytest # type: ignore
from src.yaz_pyotp.core.factory import OTPFactory
from src.yaz_pyotp.core.otp import LoginConfirmation, TwoFASetup, PasswordReset, AccountConfirmation

def test_create_login_confirmation():
    otp = OTPFactory.createOTP('login')
    assert isinstance(otp, LoginConfirmation)
    assert otp.kind == "login"

def test_create_2fa_setup():
    otp = OTPFactory.createOTP('2fa_setup')
    assert isinstance(otp, TwoFASetup)
    assert otp.kind == "2fa_setup"

def test_create_password_reset():
    otp = OTPFactory.createOTP('password_reset')
    assert isinstance(otp, PasswordReset)
    assert otp.kind == "password_reset"

def test_create_account_confirmation():
    otp = OTPFactory.createOTP('account_confirmation')
    assert isinstance(otp, AccountConfirmation)
    assert otp.kind == "account_confirmation"

def test_create_invalid_kind():
    with pytest.raises(ValueError) as e:
        OTPFactory.createOTP('invalid_kind')
    assert "invalid_kind is not a valid OTP Product" in str(e.value)

