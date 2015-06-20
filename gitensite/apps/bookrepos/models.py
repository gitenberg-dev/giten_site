#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64

# from django.utils import timezone
from django.db import models

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
