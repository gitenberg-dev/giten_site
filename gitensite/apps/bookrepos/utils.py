#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .forms import BookRepoForm
from .models import BookRepo
from .interfaces import GithubToBookRepoInterface

class GitHubOrg(object):
    """docstring for GitHubOrg"""
    def __init__(self, arg):
        super(GitHubOrg, self).__init__()
        self.arg = arg

class CommitTree():
    """
    Takes a github3.py Tree and provides interfaces
    http://github3py.readthedocs.org/en/latest/git.html#github3.git.Tree
    """
    def __init__(self, tree):
        self.tree = tree
        self.dict = self.tree.as_dict()

class BookRepoGenerator():
    """
    """
    # TODO: if there is a
    #
    def __init__(self, org):
        self.org = org

    def run(self, save=True, max_count=100):
        repo_iterator = self.org.repositories(number=max_count)
        etag = repo_iterator.etag

        for repo in repo_iterator:
            # TODO: fetch existing book as update form
            interface = GithubToBookRepoInterface(repo)
            book_repo = interface.fulfill()
            print interface
            book_repo.save()


def fetch_repos(org):
    repo_gen = BookRepoGenerator(org)
    repo_gen.run()
