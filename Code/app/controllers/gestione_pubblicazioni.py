from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.services.ai_service import AIService
from app.models.post import Post
from app import db
from config import SCORE_THRESHOLD
pubblicazioni_bp = Blueprint("pubblicazioni",  __name__)
ai_service = AIService()

#---------- VIEW ----------,
@pubblicazioni_bp.route("/feed")
def feed():
    if "user_id" not in session:
        return redirect("/login")

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
    return render_template("user/new_post.html")

#---------- API ----------,
@pubblicazioni_bp.route("/posts", methods=["POST"])
def create_post():
    if "user_id" not in session:
        return jsonify({"error": "Non autenticato"}), 401

    data = request.get_json()

    score, ai_log = ai_service.analyze_text(data["testo"])

    # TESTO NON VALIDO (casuale, lingua errata, troppo corto)
    if score < 0:
        return jsonify({
            "error": "Il testo inserito non è valido o non è semanticamente coerente"
        }), 400

    # decisione IA
    stato = "pubblicato" if score >= SCORE_THRESHOLD else "bloccato"

    post = Post(
        titolo=data["titolo"],
        testo=data["testo"],
        img_url=data.get("img_url"),
        stato=stato,
        ai_score=score,
        ai_log=ai_log,
        account_id=session["user_id"]
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        "message": "Post creato",
        "stato": stato,
        "score": round(score, 3)
    }), 201