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
        direct_set = ('clone_url', 'name', 'open_issues', 'html_url')
        for key in direct_set:
            setattr(self.book_repo, key, self.repo.__dict__[key])

        # import a stock cover for now
        self.book_repo.cover_url = 'http://placehold.it/140x200'

        # properties derived from methods
        contrib = [contrib.login for contrib in self.repo.contributors()]
        contrib = ', '.join(contrib)
        self.book_repo.contributors = contrib


        return self.book_repo

    def __str__(self):
        return "A BookRepo: " + self.book_repo.name + str(self.book_repo.open_issues)
