import os

class Config:
    """Base configuration class."""
    SERVER_NAME = os.environ.get("SERVER_NAME", '127.0.0.1:8003')
    YC_FOLDER_ID = os.environ.get("YC_FOLDER_ID")
    MODEL_NAME = "yandexgpt-lite"

    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
    }


class DevelopmentConfig(Config):
    """Development configuration."""
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True


class ProductionConfig(Config):
    """Production configuration."""
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
