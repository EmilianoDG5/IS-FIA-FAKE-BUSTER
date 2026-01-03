from flask import Blueprint, request, jsonify
from app.models.appello import Appello
from app.models.post import Post
from app import db

appelli_bp = Blueprint("appelli", __name__)


@appelli_bp.route("/appelli", methods=["POST"])
def crea_appello():
    data = request.get_json()

    post_id = data.get("post_id")
    motivazione = data.get("motivazione")

    post = Post.query.get(post_id)

    if not post or post.stato != "bloccato":
        return jsonify({"error": "Appello non consentito"}), 400

    if Appello.query.filter_by(post_id=post_id, stato="aperto").first():
        return jsonify({"error": "Appello già esistente"}), 409

    appello = Appello(
        post_id=post_id,
        motivazione=motivazione,
        stato="aperto"
    )

    db.session.add(appello)
    db.session.commit()

    return jsonify({"message": "Appello inviato"}), 201
