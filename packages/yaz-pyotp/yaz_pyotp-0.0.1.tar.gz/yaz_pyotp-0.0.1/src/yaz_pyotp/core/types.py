from typing import Protocol, Literal


class CreateRecordCallable(Protocol):
    """
    A protocol for a callable that creates a record.

    Args:
        hashed_code (str): The hashed code to store in the record.
        kind (str): The type of the record.
        expires_in (int): The time in seconds until the record expires.

    Returns:
        bool: True if the record was created successfully, False otherwise.
    """
    def __call__(self, hashed_code: str, kind: str, expires_in: int) -> bool:
        pass

class OTPRecord:
    is_valid:bool 
    hashed_otp:str

    def __init__(self, is_valid:bool, hashed_otp:str) -> None:
        self.hashed_otp = hashed_otp
        self.is_valid = is_valid

class GetRecordCallable(Protocol):
    """
    A protocol for a callable that retrieves a record.

    Args:
        kind (str): The type of the record to retrieve.

    Returns:
        OTPRecord: The otp code associated with the given kind and validation indicating that it's not expired.
    """
    def __call__(self, kind: str) -> OTPRecord:
        pass

class DeleteRecordCallable(Protocol):
    """
    A protocol for a callable that deletes a record.

    Args:
        kind (str): The type of the record to delete.

    Returns:
        bool: True if the record was deleted successfully, False otherwise.
    """
    def __call__(self, kind: str) -> bool:
        pass

ProductKind = Literal["login","2fa_setup","password_reset","account_confirmation"]

class NotificationData:
    kind:str
    recipient:str 
    is_html:bool

    def __init__(self, kind:str, recipient:str, is_html:bool=False) -> None:
        self.is_html=is_html
        self.kind = kind
        self.recipient = recipient