#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import logging

import github3

from .models import BookRepo
from .models import GHContributor


logger = logging.getLogger(__name__)

class GHContributorInterface(object):
    def __init__(self, book_repo, repo):
        """ Takes a BookRepo and a github repository obj
        """
        self.book_repo = book_repo
        self.repo = repo

    def fulfill(self):
        for user in self.repo.contributors():
            ghc = GHContributor()

            ghc.username = user.login
            ghc.book_repo = self.book_repo
            ghc.contributions = user.contributions

            ghc.save()

class BookRepoInterface(object):

    def _get_book_id(self):
        """ get bookid out of repo.title """
        name = self.repo.name
        try:
            return int(name.split('_')[-1])
        except ValueError:
            return

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
        self.book_repo.book_id = self._get_book_id()
        self.book_repo.save()

        # self.contributorint = GHContributorInterface(self.book_repo, self.repo)
        # self.contributorint.fulfill()
        # self.book_repo.contributors = self._derive_contributor_string()


class GHSearchBookRepo(BookRepoInterface):
    """ """
    def __init__(self, repo):
        super(GHSearchBookRepo, self).__init__()
        self.repo = repo
        self.book_id = self._get_book_id()
        self.book_repo, _ = BookRepo.objects.get_or_create(book_id=self.book_id)

    def fulfill(self):
        self._do_fulfill()
        return self.book_repo

    def __repr__(self):
        return u"Interface for {0} and {1}".format(self.book_repo, self.repo)


class GithubToBookRepoInterface(BookRepoInterface):
    """
    Takes a github3.Repository
    prepares a BookRepo model instance
    """
    def __init__(self, repo):
        """ takes: a Github3.Repoitory """
        self.repo = repo
        self.book_repo = BookRepo()

    def _get_bookid(self):
        """ get bookid out of repo.title """
        name = self.repo.name
        try:
            return int(name.split('_')[-1])
        except ValueError:
            return

    def fulfill(self):
        try:
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
        self.book_repo.book_id = self._get_bookid()

    def __str__(self):
        return "A BookRepo: " + self.book_repo.name + str(self.book_repo.open_issues)
