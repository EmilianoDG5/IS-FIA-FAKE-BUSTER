from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    db.init_app(app)
    migrate.init_app(app, db)

    # Import modelli
    from app.models import account, post, appello, segnalazione

    # Import blueprint
    from app.controllers.gestione_pubblicazioni import pubblicazioni_bp
    app.register_blueprint(pubblicazioni_bp)

    return app
