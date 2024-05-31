# tests/conftest.py
import pytest
from unittest.mock import Mock
from src.yaz_pyotp.settings import Settings
# from src.pyotp_client.core.types import ProductKind

Settings.set(secret_key="")

@pytest.fixture
def mock_create():
    return Mock(return_value=True)

@pytest.fixture
def mock_get():
    return Mock(return_value=Mock(otp="hashed_code", is_valid=True))

@pytest.fixture
def mock_delete():
    return Mock(return_value=True)
