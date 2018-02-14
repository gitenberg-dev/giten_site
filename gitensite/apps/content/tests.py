# invoke with ./manage.py test gitensite.apps.content or ./manage.py test

from django.test import TestCase
from django.test.client import Client

from gitensite.apps.bookinfo.models import Author, Book, Cover

import os

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

        #Test to ensure that secret is in environment variables
        self.assertEqual("GITENBERG_SECRET" in os.environ, True)

        yaml = """_repo: testbook
creator:
  author:
    agent_name: Austen, Jane
    birthdate: 1775
    deathdate: 1817
    gutenberg_agent_id: '68'
    url: http://www.gutenberg.org/2009/agents/68
    wikipedia: http://en.wikipedia.org/wiki/Jane_Austen
gutenberg_bookshelf:
- Best Books Ever Listings
- Harvard Classics
gutenberg_issued: '1998-06-01'
gutenberg_type: Text
identifiers:
  gutenberg: '1234223423'
language: en
publisher: Project Gutenberg
rights: Public domain in the USA.
rights_url: http://creativecommons.org/about/pdm
subjects:
- '!lcsh: Love stories'
- '!lcc: PR'
- '!lcsh: Domestic fiction'
- '!lcsh: Young women -- Fiction'
- '!lcsh: England -- Fiction'
- '!lcsh: Social classes -- Fiction'
- '!lcsh: Courtship -- Fiction'
- '!lcsh: Sisters -- Fiction'
title: Pride and Prejudice
url: http://www.gutenberg.org/ebooks/1342"""

        r = anon_client.post("/books/post/", data=yaml, content_type='application/octet-stream', HTTP_X_GITENBERG_SECRET=os.environ["GITENBERG_SECRET"])
        self.assertEqual(r.status_code, 200)

        book = Book.objects.get(title="Pride and Prejudice")
        self.assertEqual(book.title, "Pride and Prejudice")

        author = Author.objects.get(name="Austen, Jane")
        self.assertEqual(author.name, "Austen, Jane")
        