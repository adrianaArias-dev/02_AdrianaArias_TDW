from flask import Flask

from .config import Config
from .database import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    from .routes.imagenes import imagenes_bp
    app.register_blueprint(imagenes_bp)

    return app
