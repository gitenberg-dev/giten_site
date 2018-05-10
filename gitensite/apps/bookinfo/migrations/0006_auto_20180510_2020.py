# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookinfo', '0005_auto_20180501_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cover',
            name='file',
            field=models.FileField(max_length=500, null=True, upload_to=b'bookcovers/', blank=True),
        ),
    ]
