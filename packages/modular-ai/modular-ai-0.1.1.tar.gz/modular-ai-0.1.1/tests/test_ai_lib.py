import unittest
import os
from ailib.ai_models import AIModel
from ailib.models import Models
import requests


class TestAIModel(unittest.TestCase):

    def setUp(self):
        self.available_apis = [
            api
            for api, (key, url, _, _) in AIModel.API_CONFIG.items()
            if os.getenv(key)
        ]

    def test_generate_text(self):
        for api in self.available_apis:
            with self.subTest(api=api):
                models = AIModel.list_available_models(api)
                if models:
                    model = AIModel(models[0], api)

                    try:
                        result = model.generate_text("Test prompt")
                        self.assertIsInstance(result, str)
                    except requests.exceptions.HTTPError as e:
                        print(f"HTTPError for API '{api}': {e}")
                        print(f"Response Content: {e.response.content}")

    def test_list_available_models(self):
        for api in self.available_apis:
            with self.subTest(api=api):
                models = AIModel.list_available_models(api)
                self.assertIsInstance(models, list)
                self.assertGreater(len(models), 0)


class TestModels(unittest.TestCase):

    def setUp(self):
        self.available_apis = [
            api
            for api, (key, url, _, _) in AIModel.API_CONFIG.items()
            if os.getenv(key)
        ]

    def test_fetch_and_register_models(self):
        for api in self.available_apis:
            with self.subTest(api=api):
                Models.fetch_and_register_models(api)
                registered_models = Models.list_models()
                self.assertIn(api, registered_models)
                self.assertGreater(len(registered_models[api]), 0)

    def test_register_and_get_model(self):
        for api in self.available_apis:
            with self.subTest(api=api):
                Models.fetch_and_register_models(api)
                registered_models = Models.list_models()
                for model_name in registered_models[api]:
                    model = Models.get_model(api, model_name)
                    self.assertIsNotNone(model)
                    self.assertEqual(model.model_name, model_name)
                    self.assertEqual(model.api, api)


if __name__ == "__main__":
    unittest.main()
