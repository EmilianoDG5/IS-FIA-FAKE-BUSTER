from app.controllers.gestione_utenza import utenza_bp
from app.controllers.gestione_pubblicazioni import pubblicazioni_bp
from app.controllers.gestione_appelli import appelli_bp
from app.controllers.gestione_segnalazioni import segnalazioni_bp

app.register_blueprint(utenza_bp)
app.register_blueprint(pubblicazioni_bp)
app.register_blueprint(appelli_bp)
app.register_blueprint(segnalazioni_bp)