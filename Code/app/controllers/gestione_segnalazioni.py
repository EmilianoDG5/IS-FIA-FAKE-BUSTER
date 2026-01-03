from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.models.segnalazione import Segnalazione
from app.models.post import Post
from app import db

segnalazioni_bp = Blueprint("segnalazioni", __name__)

# ---------- VIEW ----------

@segnalazioni_bp.route("/dashboard")
def dashboard():
    if session.get("ruolo") != "fact_checker":
        return redirect("/login")

    posts = Post.query.filter_by(stato="bloccato").all()
    return render_template("fact_checker/dashboard.html", posts=posts)


@segnalazioni_bp.route("/review/<int:post_id>")
def review_post(post_id):
    if session.get("ruolo") != "fact_checker":
        return redirect("/login")

    post = Post.query.get_or_404(post_id)
    return render_template("fact_checker/review_post.html", post=post)

# ---------- API ----------

@segnalazioni_bp.route("/segnalazioni", methods=["POST"])
def segnala_post():
    if "user_id" not in session:
        return jsonify({"error": "Non autenticato"}), 401

    data = request.form if request.form else request.get_json()
    post = Post.query.get(data.get("post_id"))

    if not post or post.stato != "pubblicato":
        return jsonify({"error": "Post non segnalabile"}), 400

    segnalazione = Segnalazione(
        post_id=post.id,
        motivo=data.get("motivo"),
        stato="aperta",
        segnalatore_id=session["user_id"]
    )

    db.session.add(segnalazione)
    db.session.commit()

    return jsonify({"message": "Segnalazione inviata"}), 201
