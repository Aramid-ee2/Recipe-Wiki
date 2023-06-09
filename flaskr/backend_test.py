from flaskr.backend import Backend
from unittest.mock import MagicMock, mock_open, patch
from google.cloud import storage
import hashlib, pytest, json


def test_sign_up():
    # Variables
    mock_storage_client = MagicMock()
    user_name = "gabriel"
    password = "terrazas"
    final_password = Backend.SALT + user_name + password
    expected_val = hashlib.sha256(final_password.encode()).hexdigest()

    # Run code we are interested in testing
    backend = Backend(mock_storage_client)
    backend.sign_up(user_name, password)

    # Assertions
    with mock_storage_client.bucket().blob().open() as mock_blob:
        assert json.loads(mock_blob.write.call_args.args[0]) == {
            "Password": expected_val,
            "Language": "English",
            "Night_Mode": False,
            "Bookmarks": [],
        }


def test_sign_in():
    user_name = "gabriel"
    password = "terrazas"
    final_password = Backend.SALT + user_name + password
    temp = hashlib.sha256(final_password.encode()).hexdigest()
    expected_val = json.dumps({
        "Password": temp,
        "Language": "English",
        "Night_Mode": False,
        "Bookmarks": [],
    })

    #creating mocks
    mock_storage_client = MagicMock()
    with mock_storage_client.bucket().blob().open() as mock_blob:
        mock_blob.read.return_value = expected_val

    backend = Backend(mock_storage_client)
    signed_in = backend.sign_in(user_name, password)

    assert signed_in == True


def test_upload():
    #Mocking
    mock_storage_client = MagicMock()
    mock_search_bucket = MagicMock()
    mock_wiki_bucket = MagicMock()
    mock_wiki_blob = MagicMock()
    mock_search_blob = MagicMock()
    mock_file = MagicMock()
    mock_file.name = "abula.html"

    mock_wiki_bucket.blob.return_value = mock_wiki_blob
    mock_search_bucket.blob.return_value = mock_search_blob
    mock_search_blob.open.return_value.__enter__.return_value.read.return_value = json.dumps(
        {
            "rice": ['Seasoned_rice.html', 'fried_rice.html'],
            "shrimp": ['shrimp_alfredo.html']
        })

    mock_storage_client.bucket.side_effect = [
        None, mock_wiki_bucket, None, mock_search_bucket, None
    ]

    # Run code we are interested in testing
    backend = Backend(mock_storage_client)
    backend.file_content_file = MagicMock()
    backend.file_content_file.return_value = "<h1> Amala </>"
    backend.update_inverted_index = MagicMock()
    backend.update_inverted_index.return_value = {
        "rice": ['Seasoned_rice.html', 'fried_rice.html'],
        "shrimp": ['shrimp_alfredo.html'],
        "amala": ['abula.html']
    }
    json_index = json.dumps({
        "rice": ['Seasoned_rice.html', 'fried_rice.html'],
        "shrimp": ['shrimp_alfredo.html'],
        "amala": ['abula.html']
    })
    backend.upload(mock_file)

    # Assertions

    mock_wiki_blob.upload_from_file.assert_called_with(
        mock_file, content_type=mock_file.content_type)
    assert backend.file_content_file.call_count == 1
    mock_search_blob.open().__enter__().write.assert_called_with(json_index)


def test_init():
    # Mock client
    mock_storage_client = MagicMock()
    # Backend instance
    backend = Backend(mock_storage_client)
    assert backend.users_bucket != None
    assert backend.wiki_info_bucket != None


def test_file_content_blob():
    #creating mocks
    mock_blob = MagicMock()
    mock_storage_client = MagicMock()

    mock_blob.name = "Tech_exchange"
    mock_blob.open.return_value.__enter__.return_value.read.return_value = 'We are going to Seattle'
    backend = Backend(mock_storage_client)
    assert backend.file_content_blob(mock_blob) == 'We are going to Seattle'


def test_file_content_file():
    mock_storage_client = MagicMock()
    mock_open = MagicMock()
    mock_file = MagicMock()
    mock_file.name = 'new_recipe.html'

    mock_open.return_value.__enter__.return_value = mock_file
    mock_file.read.return_value = 'Cooking seafood'
    backend = Backend(mock_storage_client, mock_open)

    assert backend.file_content_file(mock_file) == 'Cooking seafood'


def test_get_wiki_page():
    #Mocking
    mock_user = MagicMock()
    mock_user.get_id.return_value = "aramide#"

    mock_user_bucket = MagicMock()
    mock_user_blob = MagicMock()
    mock_user_bucket.blob.return_value = mock_user_blob
    mock_user_blob.download_as_string.return_value = json.dumps({
        "Password": 'hashedword',
        "Language": "French",
        "Night_Mode": False,
        "Bookmarks": []
    })
    mock_wiki_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_wiki_bucket.blob.return_value = mock_blob
    mock_blob.name = 'French/some_page'
    mock_blob.open.return_value.__enter__.return_value.read.return_value = 'some content'


def test_get_all_page_names():
    #creating mocks
    mock_user = MagicMock()
    mock_user.get_id.return_value = "aramide#"

    mock_user_bucket = MagicMock()
    mock_user_blob = MagicMock()
    mock_user_bucket.blob.return_value = mock_user_blob
    mock_user_blob.download_as_string.return_value = json.dumps({
        "Password": 'hashedword',
        "Language": "Italian",
        "Night_Mode": False,
        "Bookmarks": []
    })
    mock_wiki_bucket = MagicMock()
    mock_blob1 = MagicMock()
    mock_blob2 = MagicMock()
    mock_wiki_bucket.list_blobs.return_value = [mock_blob1, mock_blob2]
    mock_blob1.name = 'Italian/some_page'
    mock_blob2.name = 'Italian/another_page'

    mock_storage_client = MagicMock()
    mock_storage_client.bucket.side_effect = [
        mock_user_bucket, mock_wiki_bucket, None, None, None
    ]

    backend = Backend(mock_storage_client)
    page_names = backend.get_all_page_names(mock_user)

    assert page_names == ['some_page', 'another_page']


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


def test_update_inverted_index():
    mock_storage_client = MagicMock()
    mock_file = MagicMock()
    mock_file.name = 'food.html'
    inverted_index = {}
    file_content = "<h1>Welcome Three Engineers wiki!</h1>"

    expected_index = {
        'welcome': ['food.html'],
        'three': ['food.html'],
        'engineers': ['food.html'],
        'wiki': ['food.html']
    }
    mock_soup = MagicMock()
    mock_soup.get_wiki_page.return_value = "Welcome Three Engineers wiki!"

    mock_re = MagicMock()
    mock_re.findall.return_value = ['Welcome', 'Three', 'Engineers', 'wiki']

    backend = Backend(mock_storage_client)

    assert backend.update_inverted_index(inverted_index, mock_file.name,
                                         file_content) == expected_index


def test_initial_index():
    inverted_index = {}

    #mocking and return values
    mock_storage_client = MagicMock()

    mock_wiki_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_blob.name = 'greetings.html'
    mock_wiki_bucket.list_blobs.return_value = [mock_blob]

    mock_search_bucket = MagicMock()
    mock_blob2 = MagicMock()
    mock_search_bucket.blob.return_value = mock_blob2

    mock_storage_client.bucket.side_effect = [
        None, mock_wiki_bucket, None, mock_search_bucket, None
    ]

    # Act
    backend = Backend(mock_storage_client)
    backend.file_content_blob = MagicMock()
    backend.file_content_blob.return_value = "<h1> hello </>"
    backend.update_inverted_index = MagicMock()
    backend.update_inverted_index.return_value = {"hello": ['greetings.html']}

    json_index = '{"hello": ["greetings.html"]}'
    backend.initial_index()

    #Assert
    assert backend.file_content_blob.call_count == 1
    mock_blob2.open().__enter__().write.assert_called_with(json_index)


def test_search():

    mock_storage_client = MagicMock()
    mock_search_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_search_bucket.blob.return_value = mock_blob
    mock_blob.open.return_value.__enter__.return_value.read.return_value = json.dumps(
        {
            "rice": ['Seasoned_rice.html', 'fried_rice.html'],
            "shrimp": ['shrimp_alfredo.html']
        })

    mock_storage_client.bucket.side_effect = [
        None, None, None, mock_search_bucket, None
    ]
    backend = Backend(mock_storage_client)

    assert backend.search("rice") == {'Seasoned_rice.html', 'fried_rice.html'}


def test_update_language():
    # Variables
    user_name = "gabriel"
    password = "terrazas"
    final_password = Backend.SALT + user_name + password
    expected_val = hashlib.sha256(final_password.encode()).hexdigest()

    # Mocks
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_user = MagicMock()
    mock_blob = MagicMock()

    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.download_as_string.return_value = '{"Password": \"' + expected_val + '\", "Language": "English", "Night_Mode": false, "Bookmarks": []}'

    # Testing Code
    backend = Backend(mock_storage_client)
    backend.update_language("Italian", mock_user)

    final_val = '{"Password": \"' + expected_val + '\", "Language": "Italian", "Night_Mode": false, "Bookmarks": []}'
    with mock_storage_client.bucket().blob().open() as mock_blob:
        mock_blob.write.assert_called_with(final_val)


def test_update_night_mode():
    # Variables
    user_name = "gabriel"
    password = "terrazas"
    final_password = Backend.SALT + user_name + password
    expected_val = hashlib.sha256(final_password.encode()).hexdigest()

    # Mocks
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_user = MagicMock()
    mock_blob = MagicMock()

    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.download_as_string.return_value = '{"Password": \"' + expected_val + '\", "Language": "English", "Night_Mode": false, "Bookmarks": []}'

    # Testing Code
    backend = Backend(mock_storage_client)
    backend.update_night_mode(mock_user)

    final_val = '{"Password": \"' + expected_val + '\", "Language": "English", "Night_Mode": true, "Bookmarks": []}'
    with mock_storage_client.bucket().blob().open() as mock_blob:
        mock_blob.write.assert_called_with(final_val)


def test_update_bookmarks():
    # Variables
    user_name = "gabriel"
    password = "terrazas"
    final_password = Backend.SALT + user_name + password
    expected_val = hashlib.sha256(final_password.encode()).hexdigest()

    # Mocks
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_user = MagicMock()
    mock_blob = MagicMock()

    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.download_as_string.return_value = '{"Password": \"' + expected_val + '\", "Language": "English", "Night_Mode": false, "Bookmarks": []}'

    # Testing Code
    backend = Backend(mock_storage_client)
    backend.update_bookmarks("some_page", mock_user)

    final_val = '{"Password": \"' + expected_val + '\", "Language": "English", "Night_Mode": false, "Bookmarks": ["some_page"]}'
    with mock_storage_client.bucket().blob().open() as mock_blob:
        mock_blob.write.assert_called_with(final_val)


def test_get_current_settings():
    # Variables
    user_name = "gabriel"
    password = "terrazas"
    final_password = Backend.SALT + user_name + password
    expected_val = hashlib.sha256(final_password.encode()).hexdigest()

    # Mocks
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_user = MagicMock()
    mock_blob = MagicMock()

    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.download_as_string.return_value = '{"Password": \"' + expected_val + '\", "Language": "English", "Night_Mode": false, "Bookmarks": []}'

    # Testing Code
    backend = Backend(mock_storage_client)
    assert_val = backend.get_current_settings(mock_user)

    final_val = {'Bookmarks': [], 'Language': 'English', 'Night_Mode': False}
    assert final_val == assert_val


def test_update_review():
    # Variables
    test_page = "some_page"
    test_reviews = [1, 2]
    review = 3
    updated_reviews = str([1, 2, 3])

    # Mocks
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()

    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.download_as_string.return_value = str(test_reviews)

    # Testing Code
    backend = Backend(mock_storage_client)
    backend.update_review(review, test_page)

    with mock_storage_client.bucket().blob().open() as mock_blob:
        mock_blob.write.assert_called_with(updated_reviews)


def test_view_current_reviews():
    # Variables
    test_page = "some_page"
    test_reviews = [1, 2, 3]
    test_average = 2

    # Mocks
    mock_storage_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()

    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.download_as_string.return_value = str(test_reviews)

    # Testing Code
    backend = Backend(mock_storage_client)
    final_val = backend.view_current_reviews(test_page)

    assert test_average == final_val
