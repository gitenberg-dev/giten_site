# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepos', '0012_bookrepo_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='GHContributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255, null=True, blank=True)),
                ('contributions', models.IntegerField(default=0, null=True, blank=True)),
                ('book_repo', models.ForeignKey(to='bookrepos.BookRepo')),
            ],
        ),
    ]
