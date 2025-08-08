from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow requests from frontend

    from .routes import receipts_bp
    app.register_blueprint(receipts_bp, url_prefix="/api/receipts")

    return app
