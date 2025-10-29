import os

class Config:
    SERVER_NAME = '127.0.0.1:8001'
    DEBUG = False
    TESTING = False
    COLLECTION_NAME=os.environ.get("COLLECTION_NAME", "data")
    QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")

    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
    }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
