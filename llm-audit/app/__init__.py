import os
from flask import Flask
from app.utils import exceptions, middleware, logging_config
from flasgger import Swagger


def create_app(config_name=None):
    # Load configuration based on environment
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    # Import config after app creation to avoid circular imports
    from config import config

    app = Flask(__name__)
    Swagger(app)
    app.config.from_object(config[config_name])

    logging_config.configure_logging(app)
    middleware.add_middleware(app)
    exceptions.register_error_handlers(app)

    from app.routes import estimation, health

    with app.app_context():
        app.register_blueprint(estimation.estimation_blueprint)
        app.register_blueprint(health.health_blueprint)

    return app
