#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import shared_task


@shared_task
def foo():
    pass
