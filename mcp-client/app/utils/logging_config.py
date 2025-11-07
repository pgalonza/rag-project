import os
import logging
from flask import has_request_context, g
from flask.logging import default_handler


class RequestIdFormatter(logging.Formatter):
    """
    Custom formatter that adds request ID to log records.
    """
    def format(self, record):
        if has_request_context() and hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = 'N/A'

        return super().format(record)


def configure_logging(app):
    """
    Configure Flask's built-in logger with custom formatter that includes request IDs.
    """
    # Create the custom formatter
    formatter = RequestIdFormatter(
        fmt="%(asctime)s %(process)d %(name)s %(levelname)s %(funcName)s [%(request_id)s] %(message)s",
        datefmt="%d-%b-%y %H:%M:%S"
    )

    # Get Flask's built-in logger
    app_logger = app.logger

    # Remove default handlers to avoid duplicate logs
    # app_logger.handlers.clear()
    app.logger.removeHandler(default_handler)

    # Create a new handler with our custom formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Add the handler to the app logger
    app_logger.addHandler(handler)

    # Set the logging level
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    app_logger.setLevel(log_level)

    # Ensure propagation is set correctly
    app_logger.propagate = False

    return app_logger
