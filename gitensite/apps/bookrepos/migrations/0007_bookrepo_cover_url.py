# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepos', '0006_remove_bookrepo_repo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrepo',
            name='cover_url',
            field=models.URLField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
