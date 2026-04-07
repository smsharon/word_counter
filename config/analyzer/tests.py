from django.test import TestCase
from django.urls import reverse
import json


class AnalyzeTextTest(TestCase):

    def test_valid_text(self):
        response = self.client.post(
            '/analyze-text/',
            data=json.dumps({"text": "Hello world"}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("word_count", response.json())


    def test_empty_text(self):
        response = self.client.post(
            '/analyze-text/',
            data=json.dumps({"text": ""}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        response = self.client.post(
            '/analyze-text/',
            data="invalid json",
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)            


class HistoryTest(TestCase):

    def test_get_empty_history(self):
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)