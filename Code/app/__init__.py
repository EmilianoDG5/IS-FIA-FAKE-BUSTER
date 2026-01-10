from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("config")

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    if not app.config.get("TESTING"):
        migrate.init_app(app, db)

    from app.controllers.gestione_utenza import utenza_bp
    from app.controllers.gestione_pubblicazioni import pubblicazioni_bp
    from app.controllers.gestione_appelli import appelli_bp
    from app.controllers.gestione_segnalazioni import segnalazioni_bp

    app.register_blueprint(utenza_bp)
    app.register_blueprint(pubblicazioni_bp)
    app.register_blueprint(appelli_bp)
    app.register_blueprint(segnalazioni_bp)

    return app
