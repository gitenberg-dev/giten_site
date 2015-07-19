#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.db import models

logger = logging.getLogger(__name__)

class Book(models.Model):
    book_id = models.IntegerField(unique=True)
    repo_name = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=1000, default="", db_index=True,)
    language = models.CharField(max_length=5, default="en", null=False, db_index=True,)
    description = models.TextField(default="", null=True, blank=True, db_index=True,)
    yaml = models.TextField(null=True,default="")

    def __unicode__(self):
        return self.name


