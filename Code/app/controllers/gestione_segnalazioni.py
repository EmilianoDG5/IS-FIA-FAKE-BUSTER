from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.models.segnalazione import Segnalazione
from app.models.post import Post
from app import db
from app.models.appello import Appello
segnalazioni_bp = Blueprint("segnalazioni", __name__)

# ---------- VIEW ----------

@segnalazioni_bp.route("/dashboard")
def fact_checker_dashboard():
    if "user_id" not in session or session.get("ruolo") != "fact_checker":
        return redirect("/login")

    appelli = Appello.query.filter_by(stato="aperto").all()
    segnalazioni = Segnalazione.query.filter_by(stato="aperta").all()

    return render_template(
        "fact_checker/dashboard.html",
        appelli=appelli,
        segnalazioni=segnalazioni
    )
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

    motivo = request.form.get("motivo")

    segnalazione = Segnalazione(
        post_id=post_id,
        segnalatore_id=session["user_id"],
        motivo=motivo,
        stato="aperta"
    )

    db.session.add(segnalazione)
    db.session.commit()

    return redirect("/feed")
# ===== DECISIONE SU SEGNALAZIONE =====

@segnalazioni_bp.route("/fact_checker/segnalazioni/publish/<int:seg_id>", methods=["POST"])
def fact_checker_publish_segnalazione(seg_id):
    if session.get("ruolo") != "fact_checker":
        return redirect("/login")

    seg = Segnalazione.query.get_or_404(seg_id)

    seg.post.stato = "pubblicato"
    seg.stato = "chiusa"
    seg.esito = "pubblicato"
    seg.fact_checker_id = session["user_id"]

    db.session.commit()
    return redirect("/dashboard")


@segnalazioni_bp.route("/fact_checker/segnalazioni/block/<int:seg_id>", methods=["POST"])
def fact_checker_block_segnalazione(seg_id):
    if session.get("ruolo") != "fact_checker":
        return redirect("/login")

    seg = Segnalazione.query.get_or_404(seg_id)

    seg.post.stato = "bloccato"
    seg.stato = "chiusa"
    seg.esito = "bloccato"
    seg.fact_checker_id = session["user_id"]

    db.session.commit()
    return redirect("/dashboard")

