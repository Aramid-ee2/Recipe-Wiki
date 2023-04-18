from flaskr.backend import Backend
from unittest.mock import MagicMock, mock_open, patch
from google.cloud import storage
import hashlib
import pytest
from json import dumps


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


# TODO fix test
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

# #fix test
# def test_upload():
#     #Mocking 
    
#     mock_storage_client = MagicMock()  
#     mock_search_bucket = MagicMock()
#     mock_wiki_bucket = MagicMock()
#     mock_wiki_blob = MagicMock()    
#     mock_search_blob = MagicMock()    
#     mock_file = MagicMock()

#     mock_wiki_bucket.blob.return_value = mock_wiki_blob
#     mock_search_bucket.blob.return_value = mock_search_blob
#     mock_search_blob.open.return_value.__enter__.return_value.read.return_value = dumps({
#         "rice": ['Seasoned_rice.html','fried_rice.html'],
#         "shrimp": ['shrimp_alfredo.html']
#     })       
#     mock_storage_client.bucket.side_effect = [None, mock_wiki_bucket, None,mock_search_bucket]
#     # Run code we are interested in testing
#     backend = Backend(mock_storage_client)
#     backend.upload(mock_file)

#     # Assertions
#     # mock_storage_client.bucket().blob().upload_from_file.assert_called_with(
#     #     mock_file, content_type=mock_file.content_type)
#     mock_wiki_blob.upload_from_file.assert_called_with(mock_file, content_type=mock_file.content_type)


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

#fix test
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
    mock_user_blob.download_as_string.return_value = dumps({
        "Password": 'hashedword',
        "Language": "French",
        "Night_Mode": False,
        "Bookmarks": []
    })
    mock_wiki_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_wiki_bucket.list_blobs.return_value = [mock_blob]
    mock_blob.name = 'French/some_page'
    mock_blob.open.return_value.__enter__.return_value.read.return_value = 'some content'    
    
    mock_storage_client = MagicMock()
    mock_storage_client.bucket.side_effect = [mock_user_bucket, mock_wiki_bucket, None, None]
    

    backend = Backend(mock_storage_client)
    assert backend.get_wiki_page('some_page',mock_user) == 'some content'

def test_get_all_page_names():
    #creating mocks
    mock_user = MagicMock()
    mock_user.get_id.return_value = "aramide#"

    mock_user_bucket = MagicMock()
    mock_user_blob = MagicMock()
    mock_user_bucket.blob.return_value = mock_user_blob
    mock_user_blob.download_as_string.return_value = dumps({
        "Password": 'hashedword',
        "Language": "Italian",
        "Night_Mode": False,
        "Bookmarks": []
    })
    mock_wiki_bucket = MagicMock()
    mock_blob1 = MagicMock()
    mock_blob2 = MagicMock()
    mock_wiki_bucket.list_blobs.return_value = [mock_blob1,mock_blob2]
    mock_blob1.name = 'Italian/some_page'
    mock_blob2.name = 'Italian/another_page'
   
    mock_storage_client = MagicMock()
    mock_storage_client.bucket.side_effect = [mock_user_bucket, mock_wiki_bucket, None, None]
    
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


def test_create_inverted_index():
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

    assert backend.create_inverted_index(mock_file, inverted_index,
                                         mock_file.name, file_content) == expected_index


#fix test
# def test_initial_index():
#     inverted_index = {}

#     #mocking and return values 
#     mock_storage_client = MagicMock()

#     mock_wiki_bucket = MagicMock()
#     mock_blob = MagicMock()
#     mock_blob.name = 'greetings.html'
#     mock_wiki_bucket.list_blobs.return_value = [mock_blob]
        
#     mock_search_bucket = MagicMock()
#     mock_blob2 = MagicMock()
#     mock_search_bucket.blob.return_value = mock_blob2

    
#     backend = Backend(mock_storage_client)
#     mock_storage_client.bucket.side_effect = [None, mock_wiki_bucket, None,mock_search_bucket]
    
#     backend.file_content_blob = MagicMock()
#     backend.file_content_blob.return_value = "<h1> hello </>"
#     backend.create_inverted_index = MagicMock()
#     backend.create_inverted_index.return_value = {"hello" : ['greetings.html']}
    
#     json_index = '{"hello": ["greetings.html"]}'
#     mock_blob2.open().__enter__().write.assert_called_with(json_index)
    

def test_search():
    
    mock_storage_client = MagicMock()
    mock_search_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_search_bucket.blob.return_value = mock_blob
    mock_blob.open.return_value.__enter__.return_value.read.return_value = dumps({
        "rice": ['Seasoned_rice.html','fried_rice.html'],
        "shrimp": ['shrimp_alfredo.html']
    }) 

    mock_storage_client.bucket.side_effect = [None, None, None,mock_search_bucket]
    backend = Backend(mock_storage_client)

    assert backend.search("rice") == {'Seasoned_rice.html','fried_rice.html'}

#Need help with upload, initial_index,  