import os
import requests
from dotenv import load_dotenv

load_dotenv()


class AIModel:
    API_CONFIG = {
        "openai": ("OPENAI_API_KEY", "OPENAI_API_URL", "choices", "text"),
        "gemini": ("GEMINI_API_KEY", "GEMINI_API_URL", "predictions", "text"),
        "anthropic": ("ANTHROPIC_API_KEY", "ANTHROPIC_API_URL", "completions", "text"),
        "cohere": ("COHERE_API_KEY", "COHERE_API_URL", "generations", "text"),
        "google": ("GOOGLE_API_KEY", "GOOGLE_API_URL", "predictions", "text"),
    }

    def __init__(self, model_name, api):
        self.model_name = model_name
        self.api = api.lower()

        if self.api not in AIModel.API_CONFIG:
            raise ValueError(f"API '{self.api}' not supported")

        api_key_env, api_url_env, self.response_key, self.text_key = AIModel.API_CONFIG[
            self.api
        ]
        self.api_key = os.getenv(api_key_env)
        api_url_base = os.getenv(api_url_env)
        if not self.api_key or not api_url_base:
            raise ValueError(f"API key or URL for '{self.api}' not configured properly")

        self.api_url = f"{api_url_base}/completions"
        self.max_tokens = self._fetch_model_metadata().get("max_tokens", 100)

    def generate_text(self, prompt, max_tokens=None):
        if max_tokens is None:
            max_tokens = self.max_tokens

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
        }

        print(f"Request URL: {self.api_url}")
        print(f"Request Headers: {headers}")
        print(f"Request Data: {data}")

        response = requests.post(self.api_url, headers=headers, json=data)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")

        response.raise_for_status()
        return response.json()[self.response_key][0][self.text_key]

    def _fetch_model_metadata(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(
            f"{os.getenv(AIModel.API_CONFIG[self.api][1])}/models/{self.model_name}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def list_available_models(api):
        api = api.lower()
        return AIModel._make_api_call(api, "/models")

    @staticmethod
    def _make_api_call(api, endpoint):
        if api not in AIModel.API_CONFIG:
            raise ValueError(f"API '{api}' not supported")

        api_key_env, api_url_env, _, _ = AIModel.API_CONFIG[api]
        api_key = os.getenv(api_key_env)
        api_url_base = os.getenv(api_url_env)

        if not api_key or not api_url_base:
            raise ValueError(f"API key or URL for '{api}' not configured properly")

        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{api_url_base}{endpoint}", headers=headers)
        response.raise_for_status()
        return [model["id"] for model in response.json()["data"]]

    @staticmethod
    def _list_models_openai():
        return AIModel._make_api_call("openai", "/models")

    @staticmethod
    def _list_models_gemini():
        return AIModel._make_api_call("gemini", "/models")

    @staticmethod
    def _list_models_anthropic():
        import anthropic

        client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
        return client.list_models()

    @staticmethod
    def _list_models_cohere():
        return AIModel._make_api_call("cohere", "/models")

    @staticmethod
    def _list_models_google():
        return AIModel._make_api_call("google", "/models")
