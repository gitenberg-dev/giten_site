# -*- coding: utf-8 -*-
import csv
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from gitensite.apps.bookinfo.models import Author, Book, Cover, External_Link
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

                if "creator" in metadata.metadata and "author" in metadata.metadata["creator"]:
                    (author, created) = Author.objects.get_or_create(name=metadata.author)
                    if "birthdate" in metadata.metadata["creator"]["author"]:
                        author.birth_year = metadata.metadata["creator"]["author"]["birthdate"]
                    if "deathdate" in metadata.metadata["creator"]["author"]:
                        author.death_year = metadata.metadata["creator"]["author"]["deathdate"]
                    author.save()

                book.title = metadata.title
                print (book.title)
                book.language = metadata.language if isinstance(metadata.language,str) else 'mul'
                book.description = metadata.description
                book.author = author
                book.gutenberg_type = metadata.metadata["gutenberg_type"]
                if "gutenberg_bookshelf" in metadata.metadata:
                    if type(metadata.metadata["gutenberg_bookshelf"]) is str:
                        book.gutenberg_bookshelf = metadata.metadata["gutenberg_bookshelf"]
                    else:
                        book.gutenberg_bookshelf = ";".join(metadata.metadata["gutenberg_bookshelf"])
                if "subjects" in metadata.metadata:
                    if type(metadata.metadata["subjects"]) is str:
                        book.subjects = metadata.metadata["subjects"]
                    else:
                        subjectList = [x[1] for x in metadata.metadata["subjects"]]
                        book.subjects = ";".join(subjectList)
                
                book.yaml = metadata.__unicode__()
                book.save()
            except (ValueError,IndexError):
                print "!! {}".format(reponame)
                continue
        print "{} books created".format(Book.objects.count())

