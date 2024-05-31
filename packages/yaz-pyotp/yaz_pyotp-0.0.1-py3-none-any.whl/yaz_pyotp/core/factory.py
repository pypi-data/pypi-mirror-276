from . import otp
from .types import ProductKind

class OTPFactory:
    @staticmethod
    def createOTP(kind:ProductKind):
        match(kind):
            case 'login':
                return otp.LoginConfirmation()
            case '2fa_setup':
                return otp.TwoFASetup()
            case 'password_reset':
                return otp.PasswordReset()
            case 'account_confirmation':
                return otp.AccountConfirmation()
            
        raise ValueError(f"{kind} is not a valid OTP Product")
            
