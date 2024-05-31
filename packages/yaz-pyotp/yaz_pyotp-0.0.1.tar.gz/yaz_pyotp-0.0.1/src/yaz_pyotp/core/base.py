from .hasher import Hasher
from .types import CreateRecordCallable, DeleteRecordCallable, GetRecordCallable
from .types import ProductKind
from yaz_pyutils.randoms.generate import random_numbers

class OTPBase:
    length:int
    expires_in:int
    kind:ProductKind
    template: str
    subject:str

    def __init__(self,config, length,expires_in,kind,template,subject) -> None:
        self.config = config
        self.length = length
        self.expires_in = expires_in
        self.kind = kind
        self.template = template
        self.subject = subject


    def createOTP(self,onCreate:CreateRecordCallable):
        code = self.__generateOTP()
        hashed_code = Hasher.hashCode(code)
        isCreated = self.__createOTP(hashed_code=hashed_code, onCreate=onCreate)
        return isCreated, code

    def updateOTP(self, onCreate:CreateRecordCallable, onGet: GetRecordCallable, onDelete: DeleteRecordCallable):
        isGotten = self.__getOTP(onGet)
        if(isGotten):
            self.__deleteOTP(onDelete)
        return self.createOTP(onCreate)

    def verifyOTP(self, normal_otp:str, onGet: GetRecordCallable, onDelete: DeleteRecordCallable):
        otp_record = self.__getOTP(onGet)
        if otp_record.is_valid:
            isVerified = self.__compareOTPs(hashed_otp=otp_record.hashed_otp, normal_otp=normal_otp)
            if isVerified:
                self.__deleteOTP(onDelete)
            return isVerified
        return otp_record.is_valid

    def __generateOTP(self):
        return random_numbers(self.length)
    
    def __getOTP(self, onGet:GetRecordCallable):
        return onGet(self.kind)
    
    def __compareOTPs(self, hashed_otp:str, normal_otp:str):
        return Hasher.compareHash(hashed_code=hashed_otp, new_code=normal_otp)

    def __deleteOTP(self, onDelete:DeleteRecordCallable):
        return onDelete(self.kind)

    def __createOTP(self, hashed_code:str, onCreate: CreateRecordCallable):
        return onCreate(hashed_code=hashed_code, kind=self.kind, expires_in=self.expires_in)
    
    def getMessageBody(self, code):
        try:
            return self.template.format(code=code, expires_in=self.expires_in)
        except KeyError as e:
            raise KeyError(f"Missing key: {e}")






