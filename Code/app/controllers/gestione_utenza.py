from flask import Blueprint, request, jsonify, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.account import Account
from app import db
import re

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

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

@utenza_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Dati mancanti"}), 400
  

    if len(username) < 1 or len(username) > 20:
        return jsonify({"error": "Username deve avere tra 1 e 20 caratteri"}), 400

    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Formato email non valido"}), 400

  
    if len(password) < 8:
        return jsonify({"error": "Password troppo breve"}), 400

    if Account.query.filter_by(email=email).first():
        return jsonify({"error": "Email già registrata"}), 409

    account = Account(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
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