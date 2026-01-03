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

    # 🔹 IMPORT E REGISTRAZIONE BLUEPRINT
    from app.controllers.gestione_utenza import utenza_bp
    from app.controllers.gestione_pubblicazioni import pubblicazioni_bp
    from app.controllers.gestione_appelli import appelli_bp
    from app.controllers.gestione_segnalazioni import segnalazioni_bp

    app.register_blueprint(utenza_bp)
    app.register_blueprint(pubblicazioni_bp)
    app.register_blueprint(appelli_bp)
    app.register_blueprint(segnalazioni_bp)

    return app
