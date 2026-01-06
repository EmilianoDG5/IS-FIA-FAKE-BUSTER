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
    stato = "pubblicato" if score >= SCORE_THRESHOLD else "bloccato"

    post = Post(
        titolo=data["titolo"],
        testo=data["testo"],
        stato=stato,
        ai_score=score,
        ai_log=ai_log,
        account_id=session["user_id"]

    )

    db.session.add(post)
    db.session.commit()


    if stato == "bloccato":
        return jsonify({
         "stato": "bloccato",
            "post_id": post.id,
            "score": score
        }), 200

    return jsonify({
        "status": "published"
    }), 200


@pubblicazioni_bp.route("/posts/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    post = Post.query.get_or_404(post_id)

    # 🔒 sicurezza: solo il proprietario
    if post.account_id != session["user_id"]:
        return "Accesso negato", 403

    db.session.delete(post)
    db.session.commit()

    return redirect("/my_posts")
@pubblicazioni_bp.route("/my_posts")
def my_posts():
    if "user_id" not in session:
        return redirect("/login")

    posts = Post.query.filter_by(account_id=session["user_id"]).all()
    return render_template("user/my_posts.html", posts=posts)
