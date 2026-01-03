from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.models.appello import Appello
from app.models.post import Post
from app import db

appelli_bp = Blueprint("appelli", __name__)

# ---------- VIEW ----------

@appelli_bp.route("/my_posts")
def my_posts():
    if "user_id" not in session:
        return redirect("/login")

    posts = Post.query.filter_by(account_id=session["user_id"]).all()
    return render_template("user/my_posts.html", posts=posts)

# ---------- API ----------

@appelli_bp.route("/appelli", methods=["POST"])
def crea_appello():
    if "user_id" not in session:
        return jsonify({"error": "Non autenticato"}), 401

    data = request.form if request.form else request.get_json()
    post = Post.query.get(data.get("post_id"))

    if not post or post.stato != "bloccato":
        return jsonify({"error": "Appello non consentito"}), 400

    appello = Appello(
        post_id=post.id,
        motivazione=data.get("motivazione"),
        stato="aperto"
    )

    db.session.add(appello)
    db.session.commit()

    return jsonify({"message": "Appello inviato"}), 201
