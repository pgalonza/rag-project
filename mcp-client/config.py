import os

class Config:
    """Base configuration class."""
    SERVER_NAME = os.environ.get("SERVER_NAME", '127.0.0.1:8004')
    YC_FOLDER_ID = os.environ.get("YC_FOLDER_ID")
    MODEL_NAME = os.environ.get("MODEL_NAME", "yandexgpt-lite")
    LLM_MODEL_URL = f"gpt://{YC_FOLDER_ID}/{MODEL_NAME}/latest"
    LLM_BASE_URL = os.environ.get("LLM_BASE_URL", 'https://llm.api.cloud.yandex.net/v1')
    MCP_SERVERS = {
        "search_documents": {
            'transport': os.environ.get("MCP_SEARCH_DOCUMENTS_TRANSPORT", 'streamable_http'),
            'url': os.environ.get("MCP_SEARCH_DOCUMENTS_URL", 'http://localhost:3000/mcp')
        }
    }
    ASSISTENT_ROLE = os.environ.get('ASSISTENT_ROLE', "You are a friendly and competent assistant. Use available tools to fetch up‑to‑date information. If data is insufficient, admit it openly and suggest alternative approaches. Maintain a polite but engaging tone.")

    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
    }


class DevelopmentConfig(Config):
    """Development configuration."""
    TESTING = False
    DEBUG = True

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
