# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepos', '0004_bookrepo_contributors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookrepo',
            old_name='url',
            new_name='html_url',
        ),
    ]
