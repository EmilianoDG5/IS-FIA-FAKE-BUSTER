from app import db
from datetime import datetime

class Appello(db.Model):
    tablename = "appelli"

    id = db.Column(db.Integer, primary_key=True)

    data_invio = db.Column(db.DateTime, default=datetime.utcnow)
    stato = db.Column(db.String(20), nullable=False)   # aperto | chiuso
    esito = db.Column(db.String(20))                   # accettato | respinto
    motivazione = db.Column(db.Text, nullable=False)

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=False
    )

    fact_checker_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.id")
    )