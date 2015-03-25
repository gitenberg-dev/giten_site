# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepos', '0005_auto_20150325_0221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookrepo',
            name='repo_url',
        ),
    ]
