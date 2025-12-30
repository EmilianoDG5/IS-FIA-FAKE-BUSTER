from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.account import Account
from app import db

utenza_bp = Blueprint("utenza", __name__)


@utenza_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Dati mancanti"}), 400

    if Account.query.filter(
        (Account.username == username) | (Account.email == email)
    ).first():
        return jsonify({"error": "Utente già esistente"}), 409

    account = Account(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        ruolo="user"
    )

    db.session.add(account)
    db.session.commit()

    return jsonify({"message": "Registrazione avvenuta con successo"}), 201


@utenza_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    account = Account.query.filter_by(username=username).first()

    if not account or not check_password_hash(account.password_hash, password):
        return jsonify({"error": "Credenziali non valide"}), 401

    return jsonify({
        "id": account.id,
        "ruolo": account.ruolo
    })