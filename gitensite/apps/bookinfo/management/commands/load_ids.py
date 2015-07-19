# -*- coding: utf-8 -*-
import csv

from django.core.management.base import BaseCommand

from gitensite.apps.bookinfo.models import Book

class Command(BaseCommand):
    help = "load ids and repo names from Raymond's text TSV file"
    args = "<filename>"

    def handle(self, filename, *args, **kwargs):
        with open('/Users/eric/github/local/giten_site/assets/GITenberg_repos_list_2.tsv','r') as f:
            for vals in csv.reader(f,delimiter='\t', quotechar='"'):
                try:
                    (book,created) = Book.objects.get_or_create(book_id=vals[1])
                    (book.repo_name, book.title, book.language) = (vals[2],vals[3],vals[4])
                    book.save()
                except (ValueError,IndexError):
                    continue

