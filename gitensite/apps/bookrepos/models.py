#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import getpass
import logging

from django.db import models
from github3 import login

logger = logging.getLogger(__name__)

class BookRepo(models.Model):
    book_id = models.IntegerField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    html_url = models.URLField(max_length=255, null=True, blank=True)
    # add: Contributors (fkey to GithubContributor model)
    clone_url = models.URLField(max_length=255, null=True, blank=True)
    open_issues = models.IntegerField(default=0, null=True, blank=True)
    contributors = models.CharField(max_length=255, null=True, blank=True)
    cover_url = models.URLField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    etag = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name


class GHContributor(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    book_repo = models.ForeignKey(BookRepo)
    contributions = models.IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return "GHContributor {0} on {1}".format(self.username, self.book_repo.name)


class Readme(models.Model):
    text = models.TextField()

    @classmethod
    def from_base64(self, content):
        text = base64.base64decode(content)
        return Readme(text=text)


class GitHubAuthToken(models.Model):
    token = models.TextField()
    auth_id = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_token_or_login():
        # TODO: make the exception generate a token
        try:
            gh_token = GitHubAuthToken.objects.latest('created_at')
            gh = login(token=gh_token.token)
            logger.debug("Recovered gh token from db, used that to log in.")
        except GitHubAuthToken.DoesNotExist:
            logger.debug("GitHub Token not found, try running make_github_token")

            logger.info("Logging in to github but not saving token")
            gh = login(raw_input("username:"), password=getpass.getpass())

        return gh
