#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import logging

import github3

from .models import BookRepo


logger = logging.getLogger(__name__)

class GithubToBookRepoInterface():
    """
    Takes a github3.Repository
    prepares a BookRepo model instance
    """
    def __init__(self, repo, etag=None):
        """ takes: a Github3.Repoitory """
        self.repo = repo
        self.book_repo = BookRepo()

        self.etag = etag

    def _get_bookid(self):
        """ get bookid out of repo.title """
        name = self.repo.name
        try:
            return int(name.split('_')[-1])
        except ValueError:
            return

    def fulfill(self):
        try:
            logger.debug("Trying to fulfill the first book from github")
            self._do_fulfill()
            return self.book_repo
        except github3.exceptions.ForbiddenError:
            print("ERROR: likely a 403 error")
            # TODO: python sleep for a while

    def _derive_contributor_string(self):
        """ Primative version stringification of contributors to the project """
        # TODO: replace with a db model and a m2m fkey, BookRepo >< GHUsers
        contrib = [contrib.login for contrib in self.repo.contributors()]
        return ', '.join(contrib)

    def _do_fulfill(self):

        # properties of the same name in a github3.Repo & a BookRepo db model
        direct_set = ('clone_url', 'name', 'open_issues', 'html_url')
        for key in direct_set:
            setattr(self.book_repo, key, self.repo.__dict__[key])

        self.book_repo.cover_url = 'http://placehold.it/140x200'  # placeholder img
        self.book_repo.contributors = self._derive_contributor_string()
        self.book_repo.etag = self.etag  # passed to init argument

        self.book_id = self._get_bookid()

    def __str__(self):
        return "A BookRepo: " + self.book_repo.name + str(self.book_repo.open_issues)
