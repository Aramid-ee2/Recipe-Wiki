from flaskr.backend import Backend
from unittest.mock import MagicMock, mock_open, patch
from google.cloud import storage
import hashlib
import pytest

# TODO(Project 1): Write tests for Backend methods.
def test_sign_up():
    # Variables
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_file = MagicMock()
    mock_blob = MagicMock()
    user_name = "gabriel"
    password = "terrazas"
    final_password =  Backend.SALT + user_name + password
    expected_val =  hashlib.sha256(final_password.encode()).hexdigest()

    # Mock behavior
    # Calling .bucket on mock_storage_client returns another mock (mock bucket)
    mock_storage_client.bucket.return_value = mock_bucket
    # Mock open function to return mock file
    mock_blob.open('w').__enter__.return_value = mock_file 
    mock_bucket.blob.return_value = mock_blob

    # Run code we are interested in testing 
    backend = Backend(mock_storage_client)
    backend.sign_up(user_name, password)

    # Assertions
    mock_file.write.assert_called_with(expected_val)

def test_upload():
    # Variables
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_file = MagicMock()
    mock_blob = MagicMock()

    # Mock Behavior
    # Calling .bucket on mock_storage_client returns another mock (mock bucket)
    mock_storage_client.bucket.return_value = mock_bucket
    # Return mock blob when .blob is called on mock bucket
    mock_bucket.blob.return_value = mock_blob

    # Run code we are interested in testing 
    backend = Backend(mock_storage_client)
    backend.upload(mock_file)

    # Assertions
    mock_blob.upload_from_file.assert_called_with(mock_file , content_type = mock_file.content_type)

def test_init():
    # Mock client
    mock_storage_client = MagicMock()
    mock_storage_client.bucket.return_value = MagicMock()
    # Backend instance
    backend = Backend(mock_storage_client)
    assert backend.users_bucket != None
    assert backend.wiki_info_bucket != None
