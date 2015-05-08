# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepos', '0008_auto_20150508_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrepo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
