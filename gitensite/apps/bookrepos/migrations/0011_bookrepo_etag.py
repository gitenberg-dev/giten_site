# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepos', '0010_githubauthtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrepo',
            name='etag',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
