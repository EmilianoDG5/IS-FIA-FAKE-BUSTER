import uuid
from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.services.ai_service import AIService
from app.models.post import Post
from app import db
import os
import json
from config import SCORE_THRESHOLD
from flask import (
    Blueprint,
    request,
    redirect,
    session,
    current_app,
    flash
)
pubblicazioni_bp = Blueprint("pubblicazioni",  __name__)
ai_service = AIService()

#---------- VIEW ----------,
@pubblicazioni_bp.route("/feed")
def feed():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("ruolo") == "fact_checker":
        return redirect("/dashboard")

    posts = Post.query.filter_by(stato="pubblicato").all()
    return render_template(
        "user/feed.html",
        posts=posts,
        username=session.get("username")
    )

@pubblicazioni_bp.route("/new_post")
def new_post_page():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("ruolo") == "fact_checker":
        return redirect("/dashboard")

    return render_template("user/new_post.html")

#---------- API ----------,


@pubblicazioni_bp.route("/posts", methods=["POST"])
def create_post():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("ruolo") == "fact_checker":
        return redirect("/dashboard")

    titolo = request.form.get("titolo")
    testo = request.form.get("testo")

    if not titolo or not testo:
        return redirect("/new_post")

    score, ai_log = ai_service.analyze_text(testo)
    SCORE_THRESHOLD = current_app.config.get("SCORE_THRESHOLD", 0.7)

    # ===== ERRORE DI INPUT (NON IA) =====
    if score < 0:
        try:
            info = json.loads(ai_log)
            messaggio = info.get("error", "Testo non valido")
        except Exception:
            messaggio = "Testo non valido"

        flash(f"❌ Post non inviato: {messaggio}", "danger")
        return redirect("/new_post")

    # ===== DECISIONE IA =====
    stato = "bloccato" if score >= SCORE_THRESHOLD else "pubblicato"

    # ===== UPLOAD IMMAGINE =====
    image = request.files.get("image")
    filename = None

    if image and image.filename:
        ext = image.filename.rsplit(".", 1)[1].lower()
        if ext in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            filename = f"{uuid.uuid4()}.{ext}"
            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

    # ===== SALVATAGGIO POST =====
    post = Post(
        titolo=titolo,
        testo=testo,
        stato=stato,
        ai_score=score,
        ai_log=ai_log,
        img_url=filename,
        account_id=session["user_id"]
    )

    db.session.add(post)
    db.session.commit()

    # ===== UI =====
    if stato == "bloccato":
        flash(str(post.id), "ia_blocked")   # 👈 passiamo l’ID
        return redirect("/new_post")

    return redirect("/my_posts")

@pubblicazioni_bp.route("/posts/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    if session.get("ruolo") == "fact_checker":
        return redirect("/dashboard")

    post = Post.query.get_or_404(post_id)

    if post.account_id != session["user_id"]:
        return "Accesso negato", 403

    db.session.delete(post)
    db.session.commit()

    return redirect("/my_posts")


@pubblicazioni_bp.route("/my_posts")
def my_posts():
    if "user_id" not in session:
        return redirect("/login")

    if session.get("ruolo") == "fact_checker":
        return redirect("/dashboard")

    posts = Post.query.filter_by(account_id=session["user_id"]).all()
    return render_template("user/my_posts.html", posts=posts)