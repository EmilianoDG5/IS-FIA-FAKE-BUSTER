from app import db

class Appello(db.Model):
    __tablename__ = "appelli"

    id = db.Column(db.Integer, primary_key=True)
    motivazione = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)