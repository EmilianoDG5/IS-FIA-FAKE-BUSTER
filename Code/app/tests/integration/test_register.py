import json
from app.models.account import Account
from app import db


# =========================
# REGISTRAZIONE OK
# =========================
def test_register_success(client, app):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "testuser@test.it",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    assert b"Registrazione OK" in response.data

    # verifica che l'utente sia stato salvato nel DB
    with app.app_context():
        user = Account.query.filter_by(email="testuser@test.it").first()
        assert user is not None
        assert user.username == "testuser"
        assert user.ruolo == "user"


# =========================
# DATI MANCANTI
# =========================
def test_register_dati_mancanti(client):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@test.it"
            # password mancante
        }
    )

    assert response.status_code == 400
    assert b"Dati mancanti" in response.data


# =========================
# USERNAME TROPPO LUNGO
# =========================
def test_register_username_non_valido(client):
    response = client.post(
        "/register",
        json={
            "username": "x" * 30,
            "email": "test@test.it",
            "password": "password123"
        }
    )

    assert response.status_code == 400
    assert b"Username deve avere" in response.data


# =========================
# EMAIL NON VALIDA
# =========================
def test_register_email_non_valida(client):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "email_sbagliata",
            "password": "password123"
        }
    )

    assert response.status_code == 400
    assert b"Formato email non valido" in response.data


# =========================
# PASSWORD TROPPO CORTA
# =========================
def test_register_password_troppo_corta(client):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@test.it",
            "password": "123"
        }
    )

    assert response.status_code == 400
    assert b"Password troppo breve" in response.data


# =========================
# EMAIL GIÀ REGISTRATA
# =========================
def test_register_email_gia_registrata(client, app):
    with app.app_context():
        user = Account(
            username="user1",
            email="duplicate@test.it",
            password_hash="hash",
            ruolo="user"
        )
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/register",
        json={
            "username": "altro_user",
            "email": "duplicate@test.it",
            "password": "password123"
        }
    )

    data = response.get_json()

    assert response.status_code == 409
    assert data["error"] == "Email già registrata"