import os
from flask import Flask
from app.utils import exceptions, middleware, logging_config, mcp_client
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

    from app.routes import chat, health

    with app.app_context():
        mcp_client.init_agent()
        app.register_blueprint(chat.chat_blueprint)
        app.register_blueprint(health.health_blueprint)

    return app
