from django.test import TestCase
from .models import Category, Channel


class CategoryModelsTestCase(TestCase):
    def test_import_csv(self):
        pass

    def test_tree(self):
        resp = self.client.get('/polls/')
        self.assertEqual(resp.status_code, 200)
