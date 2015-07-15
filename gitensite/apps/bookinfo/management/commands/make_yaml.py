# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from gitensite.apps.bookinfo.models import Book
from gitensite.apps.bookinfo.pg_rdf import pg_rdf_to_yaml

class Command(BaseCommand):
    help = "make yaml files from rdf in the indicated 'cache' directory"
    args = "<path>"

    def handle(self, path, *args, **kwargs):
        for book in Book.objects.all():
            rdffile = path + 
            try:
                book.yaml = pg_rdf_to_yaml(rdffile,repo_name=repo_name)
                book.save()
            except IOError:
                print "couldn't read " + rdffile
                continue
