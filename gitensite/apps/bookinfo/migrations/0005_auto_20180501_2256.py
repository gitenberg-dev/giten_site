# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookinfo', '0004_auto_20180228_1951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cover',
            name='link',
        ),
        migrations.AddField(
            model_name='cover',
            name='file',
            field=models.FileField(null=True, upload_to=b'bookcovers/', blank=True),
        ),
    ]
