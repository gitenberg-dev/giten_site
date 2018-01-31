# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookinfo', '0004_remove_author_author_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='birth',
        ),
        migrations.RemoveField(
            model_name='author',
            name='death',
        ),
        migrations.AddField(
            model_name='author',
            name='birth_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='death_year',
            field=models.IntegerField(null=True),
        ),
    ]
