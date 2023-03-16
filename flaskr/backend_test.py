from flaskr.backend import Backend
from unittest.mock import MagicMock, mock_open, patch
from google.cloud import storage
import hashlib
import pytest


def test_sign_up():
    # Variables
    mock_storage_client = MagicMock()
    user_name = "gabriel"
    password = "terrazas"
    final_password =  Backend.SALT + user_name + password
    expected_val =  hashlib.sha256(final_password.encode()).hexdigest()

    # Mock behavior
    # Calling .bucket on mock_storage_client returns another mock (mock bucket)

    # Mock objects already return another mock object when you call a
    # method on them, so we don't need to set the return value to a
    # mock object like this. I've shown a more succinct way to write
    # this.

    # Run code we are interested in testing
    backend = Backend(mock_storage_client)
    backend.sign_up(user_name, password)

    # Assertions
    # When I run this test, I get a failure:
    # AssertionError: expected call not found.
    # Expected: write('d16090863d477c2627971cf87a632d9b03e23f707994a29e7bd2e9f05c1a7917')
    # Actual: not called.
    #
    # That failure is due to a bug introduced here:
    # https://git.sds-techx.in/the-three-engineers/project1_wiki_viewer/-/commit/cbad78849d275ef33b49c0693a074b625e38223d
    # which causes the backend to not use the mock object passed above.
    # With the bug fixed, this test passes.
    with mock_storage_client.bucket().blob().open() as mock_blob:
        mock_blob.write.assert_called_with(expected_val)

    # or equivalently
    mock_storage_client.bucket().blob().open().__enter__().write.assert_called_with(expected_val)

def test_sign_in():
    user_name = "gabriel"
    password = "terrazas"
    final_password =  Backend.SALT + user_name + password
    expected_val =  hashlib.sha256(final_password.encode()).hexdigest()

    #creating mocks
    mock_storage_client = MagicMock()
    with mock_storage_client.bucket().blob().open() as mock_blob:
        mock_blob.read.return_value = expected_val

    backend = Backend(mock_storage_client)
    data = backend.sign_in(user_name, password)

    # This test is passing because it's accessing the real bucket data
    # and using a real user name and password. We have some mistakes
    # in our mocking which prevents this from working without bucket
    # access.
    # I've shown how to mock this effectively.
    assert data == True

def test_upload():
    mock_storage_client = MagicMock()
    mock_file = MagicMock()

    # Run code we are interested in testing
    backend = Backend(mock_storage_client)
    backend.upload(mock_file)

    # Assertions
    # When I run this test, I get a failure:
    # ValueError: <MagicMock name='mock.filename' id='139726316316032'> could not be converted to unicode
    # The failure is again due the bug in:
    # https://git.sds-techx.in/the-three-engineers/project1_wiki_viewer/-/commit/cbad78849d275ef33b49c0693a074b625e38223d
    mock_storage_client.bucket().blob().upload_from_file.assert_called_with(
        mock_file, content_type=mock_file.content_type
    )

def test_init():
    # Mock client
    mock_storage_client = MagicMock()
    # Backend instance
    backend = Backend(mock_storage_client)
    # For tests against None, prefer the idiom:
    # assert backend.users_bucket is not None
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

    # This test only passes because we're accessing actual bucket
    # data.  The mocking performed here doesn't actually replace the
    # interactions the backend performs for the get_wiki_page method.
    # I've shown how to mock this effectively.

def test_get_all_page_names():
    #creating mocks
    mock_storage_client = MagicMock()
    mock_blob = MagicMock
    mock_blob.name = 'some page'
    mock_storage_client.list_blobs.return_value = [mock_blob]

    backend = Backend(mock_storage_client)
    page_names = backend.get_all_page_names()

    # When I run this test, I get a failure:
    # AssertionError: assert 'Carbonara.html' == 'Chicken_Tamales.html'
    # - Chicken_Tamales.html
    # + Carbonara.html
    # The order of the blobs isn't reliable. For testing things without a
    # reliable order, you can do
    # assert 'Chicken_Tamales.html' in page_names
    #
    # But fundamentally, we shouldn't be accessing the actual bucket contents in
    # our tests. The bucket contents will change as people use the wiki.
    #
    # With the bug preventing the mock client from being used fixed,
    # we get a different error:
    #
    # FAILED backend_test.py::test_get_all_page_names - IndexError: list index out of range
    #
    # Because there's an error in the mock setup.

    assert page_names == ['some page']


def test_get_image():
    #creating mocks
    mock_storage_client = MagicMock()

    mock_blob = MagicMock()
    mock_blob.name = 'aramide.png'
    with mock_blob.open() as mock_file:
        mock_file.read.return_value = 'authors image'

    mock_storage_client.list_blobs.return_value = [mock_blob]

    backend = Backend(mock_storage_client)
    assert backend.get_image(mock_blob.name) == "authors image"
    # When I run this test, I get a failure:
    # AssertionError: assert None == 'authors image'
    # +  where None = <bound method Backend.get_image of <flaskr.backend.Backend object at 0x7f14917d97c0>>('aramide.png')
    # +    where <bound method Backend.get_image of <flaskr.backend.Backend object at 0x7f14917d97c0>> = <flaskr.backend.Backend object at 0x7f14917d97c0>.get_image
    # +    and   'aramide.png' = <MagicMock name='mock.bucket().blob()' id='139726315403680'>.name
    #
    # It fails with bucket access because the name of the file in the
    # bucket is aramide.PNG It fails with a mocked storage client due
    # to mistakes in mocking.
