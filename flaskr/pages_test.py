from flaskr import create_app
import pytest
from flaskr.backend import Backend
from unittest.mock import MagicMock, mock_open, patch
from flask_login import logout_user, current_user
from flask import url_for


# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def mock_backend():
    return MagicMock(spec=Backend)


@pytest.fixture
def app(mock_backend):
    app = create_app(
        test_config={'TESTING': True},
        backend_instance=mock_backend,
    )
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# Test Home route
def test_home_page(client):
    resp = client.get("/home")
    assert resp.status_code == 200
    assert b"Home Page" in resp.data


def test_upload_page(client, mock_backend):
    mock_backend.sign_in.return_value = True

    with client:
        client.post(
            "/log_in",
            data={
                "user_name": "test_user",
                "password": "test_password"
            },
        )
        resp = client.get("/upload")
        assert resp.status_code == 200
        assert b"Upload a file:" in resp.data


# Test Sign up
def test_sign_up_page(client):
    resp = client.get("/sign_up")
    assert resp.status_code == 200
    assert b"Sign Up" in resp.data


#Test page route
def test_pages_route(client):
    response = client.get("/pages")
    assert response.status_code == 200
    assert b"<h1> Recipes</h1>" in response.data


def test_parametrized_routes(client, mock_backend):
    mock_backend.get_wiki_page.return_value = 'a great recipe'

    response = client.get("/pages/some_page")
    assert response.status_code == 200
    assert 'a great recipe' in str(response.data)


#Test about route
def test_about_route(client, mock_backend):
    mock_backend.get_image.return_value = b'some bytes'

    response = client.get("/about")
    assert response.status_code == 200
    assert b"<h3>About this Wiki</h3>" in response.data


#Test login route when successful
def test_log_in_route_success(client, mock_backend):
    mock_backend.sign_in.return_value = True

    response = client.post(
        "/log_in",
        data={
            'user_name': 'gabriel',
            'password': 'terrazas'
        },
    )
    assert response.status_code == 302
    assert response.location == "/home"


#Test login route when authentication failed
def test_log_in_route_fail(client, mock_backend):
    mock_backend.sign_in.return_value = False

    response = client.post(
        "/log_in",
        data={
            'user_name': 'aramide',
            'password': 'ogundiran'
        },
    )
    assert response.request.path == "/log_in"
    assert b"<h1>Login</h1>" in response.data
    assert current_user == None


def test_logout(client, mock_backend):
    mock_backend.sign_in.return_value = True

    with client:
        # Log in a mock user
        client.post(
            "/log_in",
            data={
                "user_name": "test_user",
                "password": "test_password"
            },
        )
        # Check that the user is logged in
        assert current_user.is_authenticated
        # Call the logout route
        response = client.get("/logout")
        # Check that the user is logged out
        assert not current_user.is_authenticated
        # Check that the response redirects to the home page
        assert response.location == "/home"
