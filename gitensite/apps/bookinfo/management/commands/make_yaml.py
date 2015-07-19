# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from gitensite.apps.bookinfo.models import Book
from gitensite.apps.bookinfo.pg_rdf import pg_rdf_to_yaml

class Command(BaseCommand):
    help = "make yaml files from rdf in the indicated 'cache' directory"
    args = "<path>"

    def handle(self, path, *args, **kwargs):
        for book in Book.objects.all():
            rdffile = path + '/epub/'+ str(book.book_id) + '/pg' + str(book.book_id) + '.rdf'
            try:
                book.yaml = pg_rdf_to_yaml(rdffile, repo_name=book.repo_name )
                book.save()
            except IOError:
                print "couldn't read " + rdffile
                continue
            except Exception,e:
                print "processing " + rdffile
                raise e