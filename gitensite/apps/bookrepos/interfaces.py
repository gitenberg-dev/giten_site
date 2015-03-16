#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import BookRepo

class GithubToBookRepoInterface():
    """
    Takes a github3.Repository
    prepares a BookRepo model instance
    """
    def __init__(self, repo):
        self.repo = repo
        self.book_repo = BookRepo()

    def fulfill(self):
        # properties of the same name repo & BookRepo
        direct_set = ('clone_url', 'name', 'open_issues')
        for key in direct_set:
            setattr(self.book_repo, key, self.repo.__dict__[key])
        return self.book_repo

    def __str__(self):
        return "A BookRepo: " + self.book_repo.name + str(self.book_repo.open_issues)
