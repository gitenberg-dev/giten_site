# invoke with ./manage.py test gitensite.apps.content or ./manage.py test

from django.test import TestCase
from django.test.client import Client

from gitensite.apps.bookinfo.models import Author, Book, Cover
from gitensite.apps.bookinfo.external import getExternalLinks

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

        yaml = """_repo: Alice-s-Adventures-in-Wonderland_11
alternative_title: Alice in Wonderland
creator:
  author:
    agent_name: Carroll, Lewis
    alias: Dodgson, Charles Lutwidge
    birthdate: 1832
    deathdate: 1898
    gutenberg_agent_id: 7
    url: http://www.gutenberg.org/2009/agents/7
    wikipedia: http://en.wikipedia.org/wiki/Lewis_Carroll
description: "See also our HTML edition: #928"
gutenberg_bookshelf: Children's Literature
gutenberg_issued: 2008-06-27
gutenberg_type: Text
identifiers:
  gutenberg: 11
language: en
publisher: Project Gutenberg
rights: Public domain in the USA.
rights_url: http://creativecommons.org/about/pdm
subjects:
- !lcc PR
- !lcsh Fantasy
- !lcc PZ
title: Alice's Adventures in Wonderland
url: http://www.gutenberg.org/ebooks/11"""

        #Test submitting a book to the database via the POST route
        r = anon_client.post("/books/post/", data=yaml, content_type='application/octet-stream', secure=True)
        self.assertEqual(r.status_code, 200)  
        
        #Test retrieving a book from the database by title
        book = Book.objects.get(title="Alice's Adventures in Wonderland")
        self.assertEqual(book.title, "Alice's Adventures in Wonderland")

        #Test retrieving an author from the database by name
        author = Author.objects.get(name="Carroll, Lewis")
        self.assertEqual(author.name, "Carroll, Lewis")

        #Test external links feature
        externalLinks = getExternalLinks(book)
        self.assertTrue("Librivox" in externalLinks)
        self.assertTrue("Standard Ebooks" in externalLinks)
        