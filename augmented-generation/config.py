import os

class Config:
    """Base configuration class."""
    SERVER_NAME = '127.0.0.1:8002'
    COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "data")
    YC_FOLDER_ID = os.environ.get("YC_FOLDER_ID")
    MODEL_NAME = "yandexgpt-lite"
    MODEL_TEMPERATURE = 0.5
    QDRANT_URL = os.environ.get("QDRANT_URL")
    DOCUMENTS_SEARCH_URL = os.environ.get("DOCUMENTS_SEARCH_URL", "http://127.0.0.1:8001/api/v1/documents/search")
    LLM_ESTIMATION_URL = os.environ.get("LLM_ESTIMATION_URL", "http://127.0.0.1:8003/api/v1/estimate")
    ASSISTENT_ROLE = f"{os.environ.get('ASSISTENT_ROLE', "You're a friendly assistant.")}:\n{{context}}"

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
