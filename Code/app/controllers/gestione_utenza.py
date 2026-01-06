from flask import Blueprint, request, jsonify, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.account import Account
from app import db

utenza_bp = Blueprint("utenza",  __name__)

#---------- VIEW ----------,
@utenza_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("guest/login.html")

@utenza_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("guest/register.html")

@utenza_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

#---------- API ----------,
@utenza_bp.route("/")
def home():
    if "user_id" in session:
        # se loggato, vai dove devi andare
        if session.get("ruolo") == "fact_checker":
            return redirect("/dashboard")
        return redirect("/feed")

    return render_template("guest/home.html")
@utenza_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Dati mancanti"}), 400

    if Account.query.filter(
        (Account.username == data["username"]) |
        (Account.email == data["email"])
    ).first():
        return jsonify({"error": "Utente già esistente"}), 409

    account = Account(
        username=data["username"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        ruolo="user"
    )

    db.session.add(account)
    db.session.commit()

    return jsonify({"message": "Registrazione OK"}), 201


@utenza_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    account = Account.query.filter_by(username=data.get("username")).first()

    if not account or not check_password_hash(account.password_hash, data.get("password")):
        return jsonify({"error": "Credenziali errate"}), 401

    # SESSIONE
    session["user_id"] = account.id
    session["ruolo"] = account.ruolo
    session["username"] = account.username
  
    if account.ruolo == "fact_checker":
        return jsonify({"redirect": "/dashboard"})
    else:
        return jsonify({"redirect": "/feed"})