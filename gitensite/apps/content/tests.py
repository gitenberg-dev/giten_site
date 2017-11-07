# invoke with ./manage.py test gitensite.apps.content or ./manage.py test

from django.test import TestCase
from django.test.client import Client


class PageTests(TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_view_by_anonymous(self):
        anon_client = Client()
        r = anon_client.get("/", follow=True)
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/updates/", follow=True)
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/books/", follow=True)
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/search?q=moby+dick", follow=True)
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/get-involved/", follow=True)
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/faq/", follow=True)
        self.assertEqual(r.status_code, 200)
        r = anon_client.get("/license/", follow=True)
        self.assertEqual(r.status_code, 200)
