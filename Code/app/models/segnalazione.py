from app import db
from datetime import datetime

class Segnalazione(db.Model):
    __tablename__ = "segnalazione"  
    id = db.Column(db.Integer, primary_key=True)

    data_invio = db.Column(db.DateTime, default=datetime.utcnow)
    stato = db.Column(db.String(20), nullable=False)
    esito = db.Column(db.String(20))
    motivo = db.Column(db.String(255), nullable=False)

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=False
    )

    fact_checker_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.id")
    )

    segnalatore_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.id"),
        nullable=False
    )

    # ✅ SOLO back_populates (NO backref)
    post = db.relationship(
        "Post",
        back_populates="segnalazione"
    )
