#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import yaml as PyYAML
def default_ctor(loader, tag_suffix, node):
    return tag_suffix + ' ' + node.value
PyYAML.add_multi_constructor('!lcc', default_ctor)
PyYAML.add_multi_constructor('!lcsh', default_ctor)

from gitenberg.metadata.pandata import Pandata

from django.db import models

logger = logging.getLogger(__name__)

gh_org = 'GITenberg'

class Book(models.Model):
    book_id = models.IntegerField(unique=True)
    repo_name = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=1000, default="", db_index=True,)
    language = models.CharField(max_length=5, default="en", null=False, db_index=True,)
    description = models.TextField(default="", null=True, blank=True,)
    yaml = models.TextField(null=True, default="")

    def __unicode__(self):
        return self.repo_name
    
    @property
    def author(self):
        if self.yaml:
            try:
                obj = PyYAML.load(self.yaml)
                return obj["creator"]["author"]["agent_name"]
            except:
                return ""
        else:
            return ""

    @property
    def repo_url(self):
        return 'https://github.com/{}/{}'.format(gh_org,self.repo_name)

    @property
    def issues_url(self):
        return 'https://github.com/{}/{}/issues'.format(gh_org,self.repo_name)

    @property
    def downloads_url(self):
        return 'https://github.com/{}/{}//releases'.format(gh_org,self.repo_name)

    @property
    def pg_url(self):
        return 'https://www.gutenberg.org/ebooks/{}'.format(self.book_id)
    
    _pandata=None
    def metadata(self):
        if not self._pandata:
            self._pandata=Pandata()
            self._pandata.load(self.yaml)
        return self._pandata.metadata