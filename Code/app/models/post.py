from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    titolo = db.Column(db.String(255), nullable=False)
    testo = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(255))

    stato = db.Column(db.String(20), nullable=False)  # pubblicato | bloccato
    ai_score = db.Column(db.Float)
    ai_log = db.Column(db.Text)

    data_creazione = db.Column(db.DateTime, default=datetime.utcnow)

    account_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.id"),
        nullable=False
    )
