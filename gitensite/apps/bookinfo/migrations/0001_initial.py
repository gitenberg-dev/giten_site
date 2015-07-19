# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book_id', models.IntegerField(unique=True)),
                ('repo_name', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(default=b'', max_length=1000, db_index=True)),
                ('language', models.CharField(default=b'en', max_length=5, db_index=True)),
                ('description', models.TextField(default=b'', null=True, db_index=True, blank=True)),
                ('yaml', models.TextField(default=b'', null=True)),
            ],
        ),
    ]
