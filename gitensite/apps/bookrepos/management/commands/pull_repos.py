#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django management command invoked with:
    ./manage.py pull_repos <username>
"""
import getpass

from django.core.management.base import BaseCommand
from github3 import login

from gitensite.apps.bookrepos.utils import fetch_repos

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
        self.stdout.write('I need to log into your account:')

        if not args:
            self.stdout.write('You must supply a username, quitting')
            exit(1)

        gh = login(args[0], password=getpass.getpass())
        self.stdout.write('Login successful, beginning sync')

        org = gh.organization('gitenberg')
        fetch_repos(org)
