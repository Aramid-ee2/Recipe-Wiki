from flaskr.login import User

def test_user():
    user = User('Aramide112')
    assert user.username == "Aramide112"