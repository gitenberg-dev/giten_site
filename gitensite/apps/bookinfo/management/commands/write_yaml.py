# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from gitensite.apps.bookinfo.models import Book

import os

class Command(BaseCommand):
    help = "write yaml files from db to ./metadata/<book_id>.yaml"
    args = "<path>"

    def handle(self, path, *args, **kwargs):
        for book in Book.objects.all():
            with open(os.path.join(path,'{}.yaml'.format(book.book_id)), 'w') as _fp:
                _fp.write(book.yaml.encode("utf-8"))
