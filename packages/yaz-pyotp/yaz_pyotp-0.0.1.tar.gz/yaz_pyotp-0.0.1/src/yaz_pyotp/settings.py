
class OTPSetting:
    length:int|None
    expires_in:int|None
    template:str|None
    subject:str|None

    def __init__(self,length:int|None = None, expires_in:int|None = None, template:str|None = None, subject:str|None=None) -> None:
        self.expires_in=expires_in
        self.length=length
        self.template=template
        self.subject=subject

class Settings:
    secret_key:str
    login:OTPSetting|None
    password_reset:OTPSetting | None
    two_fa_setup:OTPSetting | None
    account_confirmation:OTPSetting | None
    
    @staticmethod
    def set(secret_key:str, 
            login:OTPSetting | None = None,
            password_reset:OTPSetting  | None = None,
            two_fa_setup:OTPSetting  | None = None,
            account_confirmation:OTPSetting | None = None,
            ):
        Settings.secret_key = secret_key
        Settings.login = login
        Settings.password_reset = password_reset
        Settings.two_fa_setup = two_fa_setup
        Settings.account_confirmation = account_confirmation
        