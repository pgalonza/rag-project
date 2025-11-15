import os
from flask import Flask
from typing import Optional
from app.utils import exceptions, middleware, logging_config, mcp_client
from flasgger import Swagger
import asyncio
from config import Config


def create_app(config_name: Optional[str] = None) -> Flask:
    # Load configuration based on environment
    if config_name is None:
        config_name: str = os.environ.get('FLASK_ENV', 'default')

    # Import config after app creation to avoid circular imports
    from config import config

    app: Flask = Flask(__name__)
    Swagger(app)
    config_obj: Config = config[config_name]
    app.config.from_object(config_obj)

    logging_config.configure_logging(app)
    middleware.add_middleware(app)
    exceptions.register_error_handlers(app)

    from app.routes import chat, health

    with app.app_context():
        loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(mcp_client.init_agent())
        loop.close()
        app.register_blueprint(chat.chat_blueprint)
        app.register_blueprint(health.health_blueprint)

    return app
