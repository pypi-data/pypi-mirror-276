from .base import OTPBase
from ..settings import Settings

class LoginConfirmation(OTPBase):
    def __init__(self) -> None:
        self.config = getattr(Settings, "login")
        super().__init__(
            config = getattr(Settings, "login"),
            length = getattr(self.config, "length", None) or 6,
            expires_in = getattr(self.config, "expires_in", None) or 3,
            kind = "login",
            template = getattr(self.config, "template", None) or "Your one-time verification code to confirm your login is {code} and it expires in {expires_in} minutes. DO NOT SHARE WITH ANYONE!",
            subject = getattr(self.config, "subject", None) or "Login Confirmation One-Time-Code"
        )

class TwoFASetup(OTPBase):
    def __init__(self) -> None:
        self.config = getattr(Settings, "two_fa_setup"),
        super().__init__(
            config = getattr(Settings, "two_fa_setup"),
            length = getattr(self.config, "length", None) or 6,
            expires_in = getattr(self.config, "expires_in", None) or 3,
            kind = "2fa_setup",
            template = getattr(self.config, "template", None) or "Your one-time verification code to set up 2FA is {code} and it expires in {expires_in} minutes. DO NOT SHARE WITH ANYONE!",
            subject = getattr(self.config, "subject", None) or "Two Factor Authentication Setup One-Time-Code"
        )

class PasswordReset(OTPBase):
        def __init__(self) -> None:
            self.config = getattr(Settings, "password_reset"),
            super().__init__(
                config = getattr(Settings, "password_reset"),
                length = getattr(self.config, "length", None) or 6,
                expires_in = getattr(self.config, "expires_in", None) or 3,
                kind = "password_reset",
                template = getattr(self.config, "template", None) or "Your one-time verification code to reset your password is {code} and it expires in {expires_in} minutes. DO NOT SHARE WITH ANYONE!",
                subject = getattr(self.config, "subject", None) or "Password Reset One-Time-Code"
            )
            

class AccountConfirmation(OTPBase):
        def __init__(self) -> None:
            self.config = getattr(Settings, "account_confirmation"),
            super().__init__(
                config = getattr(Settings, "account_confirmation"),
                length = getattr(self.config, "length", None) or 6,
                expires_in = getattr(self.config, "expires_in", None) or 3,
                kind = "account_confirmation",
                template = getattr(self.config, "template", None) or "Your one-time verification code to confirm your account is {code} and it expires in {expires_in} minutes. DO NOT SHARE WITH ANYONE!",
                subject = getattr(self.config, "subject", None) or "Account Confirmation One-Time-Code"
            )
            