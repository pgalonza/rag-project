import os
from typing import Dict, Any

class Config:
    """Base configuration class."""
    SERVER_NAME: str = os.environ.get("SERVER_NAME", '127.0.0.1:8004')
    YC_FOLDER_ID: str = os.environ.get("YC_FOLDER_ID", "")
    MODEL_NAME: str = os.environ.get("MODEL_NAME", "yandexgpt-lite")
    LLM_MODEL_URL: str = f"gpt://{YC_FOLDER_ID}/{MODEL_NAME}/latest"
    LLM_BASE_URL: str = os.environ.get("LLM_BASE_URL", 'https://llm.api.cloud.yandex.net/v1')
    MCP_SERVERS: Dict[str, Dict[str, str]] = {
        "search_documents": {
            'transport': os.environ.get("MCP_SEARCH_DOCUMENTS_TRANSPORT", 'streamable_http'),
            'url': os.environ.get("MCP_SEARCH_DOCUMENTS_URL", 'http://localhost:3000/mcp')
        }
    }
    ASSISTENT_ROLE: str = os.environ.get('ASSISTENT_ROLE', "You are a friendly and competent assistant. Use available tools to fetch up‑to‑date information. If data is insufficient, admit it openly and suggest alternative approaches. Maintain a polite but engaging tone.")

    # Security headers
    SECURITY_HEADERS: Dict[str, str] = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
    }


class DevelopmentConfig(Config):
    """Development configuration."""
    TESTING: bool = False
    DEBUG: bool = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING: bool = True


class ProductionConfig(Config):
    """Production configuration."""
    TESTING: bool = False

config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
