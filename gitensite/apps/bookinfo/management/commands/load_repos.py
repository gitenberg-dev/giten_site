from __future__ import print_function
# -*- coding: utf-8 -*-
import csv
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from gitensite.apps.bookinfo.models import Author, Book, Cover, External_Link
from gitenberg.util.catalog import BookMetadata, repo_list

from gitensite.apps.bookinfo.db import addBookFromYaml

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
                metadata=BookMetadata(Book(book_id=pg_id), rdf_library=rdf_library, enrich=should_enrich)    
                addBookFromYaml(metadata.__unicode__())
            except (ValueError,IndexError):
                print("!! {}".format(reponame))
                continue
        print ("{} books created".format(Book.objects.count()))

