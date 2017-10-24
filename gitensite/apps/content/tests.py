# invoke with ./manage.py test gitensite.apps.content or ./manage.py test

from django.test import TestCase
from django.test.client import Client


class PageTests(TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_view_by_anonymous(self):
        anon_client = Client()
        r = anon_client.get("/")
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/updates/")
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/books/")
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/search?q=moby+dick")
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/get-involved/")
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/faq/")
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/license/")
        self.assertEqual(r.status_code, 200)
