from flaskr import create_app
import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Test Main route
def test_main_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"The three engineers Wiki" in resp.data
# Test Home route
def test_home_page(client):
    resp = client.get("/home")
    assert resp.status_code == 200
    assert b"Home Page" in resp.data
# Test Upload route
def test_upload_page(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b"Upload a file:" in resp.data
# Test Sign up
def test_sign_up_page(client):
    resp = client.get("/sign_up")
    assert resp.status_code == 200
    assert b"Sign Up" in resp.data


# @app.route("/upload" , methods = ["GET" , "POST"])
#     def upload():
#         # Fix Post 
#         if request.method == "POST":
#             backend.upload(request.files['file'])
#         # Redirect user to home page after uploading a file
#         return render_template("upload.html")

# # TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# # match the changes made in the other Checkpoint Requirements.
# def test_home_page(client):
#     resp = client.get("/")
#     assert resp.status_code == 200
#     assert b"Hello, World!\n" in resp.data

