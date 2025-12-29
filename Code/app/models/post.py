from app import db

class Post(db.Model):
    tablename = "posts"

    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(255), nullable=False)
    testo = db.Column(db.Text, nullable=False)
    score_ia = db.Column(db.Float)
    stato = db.Column(db.String(20), nullable=False)  # pubblicato | bloccato
    autore_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)