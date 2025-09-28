"""Shared configuration for connecting Mem0 to Azure resources."""

from dotenv import load_dotenv
import os

# Pull secrets from the local .env so running the demo remains simple.
load_dotenv()

LLM_AZURE_OPENAI_API_KEY = os.environ["LLM_AZURE_OPENAI_API_KEY"]
LLM_AZURE_CHAT_COMPLETION_DEPLOYMENT = os.environ["LLM_AZURE_CHAT_COMPLETION_DEPLOYMENT"]
LLM_AZURE_OPENAI_ENDPOINT = os.environ["LLM_AZURE_OPENAI_ENDPOINT"]
LLM_AZURE_CHAT_COMPLETION_API_VERSION = os.environ["LLM_AZURE_CHAT_COMPLETION_API_VERSION"]
LLM_AZURE_EMBEDDING_DEPLOYMENT = os.environ["LLM_AZURE_EMBEDDING_DEPLOYMENT"]
LLM_AZURE_EMBEDDING_API_VERSION = os.environ["LLM_AZURE_EMBEDDING_API_VERSION"]
SEARCH_SERVICE_NAME = os.environ["SEARCH_SERVICE_NAME"]
SEARCH_SERVICE_API_KEY = os.environ["SEARCH_SERVICE_API_KEY"]

# Central config object consumed by Mem0 when building the memory backend.
CONFIG = {
    "llm": {
        "provider": "azure_openai",
        "config": {
            "model": LLM_AZURE_CHAT_COMPLETION_DEPLOYMENT,
            "temperature": 0.1,
            "max_tokens": 2000,
            "azure_kwargs": {
                "azure_deployment": LLM_AZURE_CHAT_COMPLETION_DEPLOYMENT,
                "api_version": LLM_AZURE_CHAT_COMPLETION_API_VERSION,
                "azure_endpoint": LLM_AZURE_OPENAI_ENDPOINT,
                "api_key": LLM_AZURE_OPENAI_API_KEY,
            },
        },
    },
    "embedder": {
        "provider": "azure_openai",
        "config": {
            "model": LLM_AZURE_EMBEDDING_DEPLOYMENT,
            "embedding_dims": 1536,
            "azure_kwargs": {
                "api_version": LLM_AZURE_EMBEDDING_API_VERSION,
                "azure_deployment": LLM_AZURE_EMBEDDING_DEPLOYMENT,
                "azure_endpoint": LLM_AZURE_OPENAI_ENDPOINT,
                "api_key": LLM_AZURE_OPENAI_API_KEY,
            },
        },
    },
    "vector_store": {
        "provider": "azure_ai_search",
        "config": {
            "service_name": SEARCH_SERVICE_NAME,
            "api_key": SEARCH_SERVICE_API_KEY,
            "collection_name": "my-demo-mem0-agent-memories",
            "embedding_model_dims": 1536,
            "compression_type": "binary",
        },
    },
}
