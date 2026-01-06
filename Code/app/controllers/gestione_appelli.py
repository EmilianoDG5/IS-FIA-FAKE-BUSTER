from flask import Blueprint, session, redirect, request

from app.models.appello import Appello
from app.models.post import Post
from app import db

appelli_bp = Blueprint(
    "appelli",
    __name__,
    url_prefix="/fact_checker/appelli"
)
@appelli_bp.route("/publish/<int:appello_id>", methods=["POST"])
def publish_appello(appello_id):
    if session.get("ruolo") != "fact_checker":
        return redirect("/login")

    appello = Appello.query.get_or_404(appello_id)
    post = Post.query.get_or_404(appello.post_id)

    post.stato = "pubblicato"
    appello.stato = "chiuso"
    appello.esito = "accettato"

    db.session.commit()
    return redirect("/dashboard")


@appelli_bp.route("/block/<int:appello_id>", methods=["POST"])
def block_appello(appello_id):
    if session.get("ruolo") != "fact_checker":
        return redirect("/login")

    appello = Appello.query.get_or_404(appello_id)
    post = Post.query.get_or_404(appello.post_id)

    post.stato = "bloccato"
    appello.stato = "chiuso"
    appello.esito = "respinto"

    db.session.commit()
    return redirect("/dashboard")

@appelli_bp.route("/create/<int:post_id>", methods=["POST"])
def crea_appello(post_id):
    if "user_id" not in session:
        return redirect("/login")

    motivazione = request.form.get("motivazione")

    if not motivazione:
        return "Motivazione mancante", 400

    appello = Appello(
        post_id=post_id,
        stato="aperto",
        motivazione=motivazione
    )

    db.session.add(appello)
    db.session.commit()

    return redirect("/my_posts")