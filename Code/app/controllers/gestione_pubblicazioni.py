gestione_pubblicazioni.py

from flask import Blueprint, request, jsonify
from app.services.ai_service import AIService
from app.models.post import Post
from app import db
from config import SCORE_THRESHOLD

pubblicazioni_bp = Blueprint("pubblicazioni", __name__)
ai_service = AIService()


@pubblicazioni_bp.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    titolo = data.get("titolo")
    testo = data.get("testo")
    img_url = data.get("img_url")
    account_id = data.get("account_id")

    if not titolo or not testo or not account_id:
        return jsonify({"error": "Dati mancanti"}), 400

    score, ai_log = ai_service.analyze_text(testo)

    stato = "pubblicato" if score >= SCORE_THRESHOLD else "bloccato"

    post = Post(
        titolo=titolo,
        testo=testo,
        img_url=img_url,
        stato=stato,
        ai_score=score,
        ai_log=ai_log,
        account_id=account_id
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        "post_id": post.id,
        "score": score,
        "stato": stato
    }), 201