from .core.factory import OTPFactory
from .core.types import ProductKind, CreateRecordCallable, NotificationData, DeleteRecordCallable, GetRecordCallable
from yaz_pynotify.notification_service.client import notify
from yaz_pynotify.messaging_service.types import MessageData

def sendOTP(otp_kind:ProductKind, notification:NotificationData, onCreate: CreateRecordCallable):
    otp_product = OTPFactory.createOTP(otp_kind)
    flag, code = otp_product.createOTP(onCreate)
    if flag:
        notify(notification.kind, data=MessageData(
            recipient=notification.recipient,
            subject=otp_product.subject,
            body=otp_product.getMessageBody(code),
            is_html=notification.is_html
        ))
    return flag

def resendOTP(otp_kind:ProductKind, notification:NotificationData, onCreate: CreateRecordCallable, onGet: GetRecordCallable, onDelete: DeleteRecordCallable):
    otp_product = OTPFactory.createOTP(otp_kind)
    flag, code = otp_product.updateOTP(onCreate=onCreate, onDelete=onDelete, onGet=onGet)
    if flag:
        notify(notification.kind, data=MessageData(
            recipient=notification.recipient,
            subject=otp_product.subject,
            body=otp_product.getMessageBody(code),
            is_html=notification.is_html
        ))
    return flag

def verifyOTP(otp_kind:ProductKind, normal_otp:str, onGet: GetRecordCallable, onDelete: DeleteRecordCallable):
    otp_product = OTPFactory.createOTP(otp_kind)
    return otp_product.verifyOTP(normal_otp=normal_otp, onDelete=onDelete, onGet=onGet)



