from flaskr.backend import Backend
from unittest.mock import MagicMock
from google.cloud import storage
import pytest

# TODO(Project 1): Write tests for Backend methods.
def test_sign_up():
    pass
def test_upload():
    pass
def test_init():
    # Mock client
    mock_storage_client = MagicMock()
    mock_storage_client.bucket.return_value = MagicMock()
    # Backend instance
    backend = Backend(mock_storage_client)
    assert backend.users_bucket != None
    assert backend.wiki_info_bucket != None
