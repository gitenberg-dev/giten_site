# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepos', '0011_bookrepo_etag'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrepo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 18, 22, 21, 0, 970969), auto_now=True),
            preserve_default=False,
        ),
    ]
