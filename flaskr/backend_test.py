from flaskr.backend import Backend
from unittest.mock import MagicMock, mock_open, patch
from google.cloud import storage
import hashlib, pytest


def test_sign_up():
    # Variables
    mock_storage_client = MagicMock()
    user_name = "gabriel"
    password = "terrazas"
    final_password = Backend.SALT + user_name + password
    expected_val = hashlib.sha256(final_password.encode()).hexdigest()
    final_val = '{"Password": \"' + expected_val + '\", "Language": "English", "Night_Mode": false, "Bookmarks": []}'

    # Run code we are interested in testing
    backend = Backend(mock_storage_client)
    backend.sign_up(user_name, password)

    # Assertions
    with mock_storage_client.bucket().blob().open() as mock_blob:
        mock_blob.write.assert_called_with(final_val)


def test_sign_in():
    user_name = "gabriel"
    password = "terrazas"
    final_password = Backend.SALT + user_name + password
    temp = hashlib.sha256(final_password.encode()).hexdigest()
    expected_val = '{"Password": \"' + temp + '\", "Language": "English", "Night_Mode": false, "Bookmarks": []}'

    #creating mocks
    mock_storage_client = MagicMock()
    with mock_storage_client.bucket().blob().open() as mock_blob:
        mock_blob.read.return_value = expected_val

    backend = Backend(mock_storage_client)
    signed_in = backend.sign_in(user_name, password)

    assert signed_in == True


def test_upload():
    mock_storage_client = MagicMock()
    mock_file = MagicMock()

    # Run code we are interested in testing
    backend = Backend(mock_storage_client)
    backend.upload(mock_file)

    # Assertions
    mock_storage_client.bucket().blob().upload_from_file.assert_called_with(
        mock_file, content_type=mock_file.content_type)


def test_init():
    # Mock client
    mock_storage_client = MagicMock()
    # Backend instance
    backend = Backend(mock_storage_client)
    assert backend.users_bucket != None
    assert backend.wiki_info_bucket != None


def test_get_wiki_page():
    mock_blob = MagicMock()
    mock_blob.name = 'some_page'
    with mock_blob.open() as mock_file:
        mock_file.read.return_value = 'some content'

    mock_storage_client = MagicMock()
    mock_storage_client.list_blobs.return_value = [mock_blob]

    backend = Backend(mock_storage_client)
    assert backend.get_wiki_page('some_page') == 'some content'


def test_get_all_page_names():
    #creating mocks
    mock_storage_client = MagicMock()
    mock_blob = MagicMock
    mock_blob.name = 'some page'
    mock_storage_client.list_blobs.return_value = [mock_blob]

    backend = Backend(mock_storage_client)
    page_names = backend.get_all_page_names()

    assert page_names == ['some page']


def test_get_image():
    #creating mocks
    mock_storage_client = MagicMock()

    mock_blob = MagicMock()
    mock_blob.name = 'an_image.png'
    with mock_blob.open() as mock_file:
        mock_file.read.return_value = 'authors image'

    mock_storage_client.list_blobs.return_value = [mock_blob]

    backend = Backend(mock_storage_client)
    assert backend.get_image(mock_blob.name) == "authors image"
