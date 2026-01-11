import pytest
from app import create_app, db
from app.models.account import Account

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def logged_user(app, client):
    with app.app_context():
        user = Account(
            username="testuser",
            email="test@test.it",
            ruolo="user",
            password_hash="fake-hash"
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id


    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["ruolo"] = "user"

    return user
