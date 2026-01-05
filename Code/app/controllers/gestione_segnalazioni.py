from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.models.segnalazione import Segnalazione
from app.models.post import Post
from app import db

segnalazioni_bp = Blueprint("segnalazioni", __name__)

# ---------- VIEW ----------

@segnalazioni_bp.route("/dashboard")
def fact_checker_dashboard():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("ruolo") != "fact_checker":
        return redirect("/login")

    posts = Post.query.filter_by(stato="bloccato").all()
    posts = (
    Post.query
    .join(Segnalazione)
    .filter(Segnalazione.stato == "aperta")
    .all()
)
    return render_template("fact_checker/dashboard.html", posts=posts)


@segnalazioni_bp.route("/review/<int:post_id>")
def fact_checker_review_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    if session.get("ruolo") != "fact_checker":
        return redirect("/login")

    post = Post.query.get_or_404(post_id)
    return render_template("fact_checker/review_post.html", post=post)

# ---------- API ----------

@segnalazioni_bp.route("/segnala/<int:post_id>", methods=["POST"])
def segnala_post_by_user(post_id):
    if "user_id" not in session:
        return redirect("/login")

    segnalazione = Segnalazione(
        post_id=post_id,
        segnalatore_id=session["user_id"],
        motivo="Contenuto sospetto",
        stato="aperta"
    )

    db.session.add(segnalazione)
    db.session.commit()

    return redirect("/feed")


@segnalazioni_bp.route("/fact_checker/publish/<int:post_id>", methods=["POST"])
def fact_checker_publish_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    if session.get("ruolo") != "fact_checker":
        return "Accesso negato", 403

    post = Post.query.get_or_404(post_id)
    post.stato = "pubblicato"

    db.session.commit()
    return redirect("/dashboard")


@segnalazioni_bp.route("/fact_checker/block/<int:post_id>", methods=["POST"])
def fact_checker_block_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    if session.get("ruolo") != "fact_checker":
        return "Accesso negato", 403

    post = Post.query.get_or_404(post_id)
    post.stato = "bloccato"

    db.session.commit()
    return redirect("/dashboard")
