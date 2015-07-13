#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django management command invoked with:
    ./manage.py pull_repos <username>
"""
from __future__ import print_function
import logging

from django.core.management.base import BaseCommand

from gitensite.apps.bookrepos.utils import SearchAllRepos

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    """
    args = "<username>"
    help = """
            Pulls info from book repositores on github
            belonging to the GITenberg organization.

            Takes:
                <username> - string of github user, will ask for password to log in
                             user doesn't have to be a member of the GITenberg org
           """

    def handle(self, *args, **options):
        repo_gen = SearchAllRepos()
        repo_gen.run()
