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

def test_sign_in():
    #creating mocks
    mock_bucket = MagicMock()
    mock_file = MagicMock()
    mock_blob = MagicMock()

    user_name = "gabriel"
    password = "terrazas"
    final_password =  Backend.SALT + user_name + password
    expected_val =  hashlib.sha256(final_password.encode()).hexdigest()    

    mock_blob.open('r').return_value.__enter__.return_value.read.return_value = expected_val

    mock_storage_client = MagicMock()
    backend = Backend(mock_storage_client)
    data = backend.sign_in(user_name, password)

    assert data == True


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

def test_get_wiki_page():
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_file = MagicMock()
    mock_blob = MagicMock()
    mock_blob.name = 'Jollof_rice.html'
    
    backend = Backend(mock_storage_client)
    page_data = backend.get_wiki_page(mock_blob.name)


    assert "<h2>Ingredients:</h2>" in page_data

def test_get_all_page_names():
#creating mocks
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_file = MagicMock()
    mock_blob = MagicMock()
    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = [mock_blob]

    backend = Backend(mock_storage_client)
    page_names = backend.get_all_page_names()

    assert page_names[0] == 'Chicken_Tamales.html'    
    

    
def test_get_image():
    #creating mocks
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_file = MagicMock()
    mock_blob = MagicMock()
    mock_blob.name = 'aramide.png'
    mock_storage_client.bucket.return_value = mock_bucket
    mock_blob.open('rb').return_value.__enter__.return_value.read.return_value = "authors image"
    mock_bucket.blob.return_value = mock_blob

    backend = Backend(mock_storage_client)
    assert backend.get_image(mock_blob.name) == "authors image"
    

    
