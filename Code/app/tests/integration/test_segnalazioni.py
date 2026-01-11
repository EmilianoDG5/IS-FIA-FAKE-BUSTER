def test_utente_non_puo_segnalare_due_volte_stesso_post(client, app):
    from app.models.account import Account
    from app.models.post import Post
    from app.models.segnalazione import Segnalazione
    from app import db
    from werkzeug.security import generate_password_hash

    with app.app_context():
        user = Account(
            username="user1",
            email="user1@test.it",
            password_hash=generate_password_hash("password123"),
            ruolo="user"
        )
        db.session.add(user)
        db.session.commit()

        post = Post(
            titolo="Post test",
            testo="Contenuto test",
            stato="pubblicato",
            ai_score=0.1,
            account_id=user.id
        )
        db.session.add(post)
        db.session.commit()

        # prima segnalazione
        segnalazione = Segnalazione(
            segnalatore_id=user.id,
            post_id=post.id,
            motivo="Prima segnalazione",
            stato="aperta"
        )
        db.session.add(segnalazione)
        db.session.commit()

        # seconda segnalazione (vietata)
        segnalazione_doppia = Segnalazione.query.filter_by(
            segnalatore_id=user.id,
            post_id=post.id
        ).first()

        assert segnalazione_doppia is not None
