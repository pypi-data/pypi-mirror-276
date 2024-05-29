from .ai_models import AIModel
import os


class Models:
    _registry = {}

    @classmethod
    def register_model(cls, provider, model_name, api):
        if provider not in cls._registry:
            cls._registry[provider] = {}
        cls._registry[provider][model_name] = AIModel(model_name, api=api)

    @classmethod
    def get_model(cls, provider, model_name):
        return cls._registry.get(provider, {}).get(model_name)

    @classmethod
    def list_models(cls):
        return cls._registry

    @classmethod
    def fetch_and_register_models(cls, api):
        provider = api.lower()
        api_key_env, api_url_env, _, _ = AIModel.API_CONFIG[api]
        if os.getenv(api_key_env) and os.getenv(api_url_env):
            models = AIModel.list_available_models(api)
            for model_name in models:
                cls.register_model(provider, model_name, api)


# Fetch and register models from each provider with configured API keys
for api in AIModel.API_CONFIG:
    Models.fetch_and_register_models(api)
