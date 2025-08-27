from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow requests from frontend

    from .routes import receipts_bp
    from .update_term_route import update_bp

    app.register_blueprint(receipts_bp, url_prefix="/api/receipts")
    app.register_blueprint(update_bp)  # Register the update term endpoint

    return app
