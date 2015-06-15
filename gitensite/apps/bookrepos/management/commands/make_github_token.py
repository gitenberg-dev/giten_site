# -*- coding: utf-8 -*-
from __future__ import print_function
from getpass import getpass

from django.core.management.base import BaseCommand
from github3 import authorize

from gitensite.apps.bookrepos.models import GitHubAuthToken


class Command(BaseCommand):
    """ Authenticate a GitHub auth token """

    def handle(self, *args, **kwargs):
        user = raw_input("GitHub username: ")
        password = ''

        while not password:
            password = getpass('Password for {0}: '.format(user))

        note = 'gitenberg website github token auth'
        note_url = 'http://www.gitenberg.org'
        scopes = ['user', 'repo']

        auth = authorize(user, password, scopes, note, note_url)
        auth_token = GitHubAuthToken(auth_id=auth.id, token=auth.token)
        auth_token.save()
