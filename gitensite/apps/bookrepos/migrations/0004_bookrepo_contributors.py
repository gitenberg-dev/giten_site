# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepos', '0003_auto_20150316_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrepo',
            name='contributors',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
