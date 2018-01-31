from __future__ import print_function
# -*- coding: utf-8 -*-
import csv
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from gitensite.apps.bookinfo.models import Book
from gitenberg.util.catalog import BookMetadata, repo_list

class Command(BaseCommand):
    help = "load ids and repo names from Raymond's text TSV file"
    args = "rdf_library", "start"
    def handle(self, rdf_library, start=0, *args, **kwargs):
        should_enrich = True
        if settings.DEBUG:
            should_enrich = False

        start = int(start)
        if start==0:
            Book.objects.all().delete()
        for (pg_id, repo_name) in repo_list:
            if int(pg_id)<start:
                continue
            try:
                (book,created) = Book.objects.get_or_create(book_id=int(pg_id), repo_name=repo_name)
                metadata=BookMetadata(book,rdf_library=rdf_library, enrich=should_enrich)
                book.language = metadata.language if isinstance(metadata.language,str) else 'mul'
                book.description = metadata.description
                book.title = metadata.title
                book.yaml = metadata.__unicode__()
                book.save()
            except (ValueError,IndexError):
                print ("!! {}".format(reponame))
                continue
        print ("{} books created".format(Book.objects.count()))

