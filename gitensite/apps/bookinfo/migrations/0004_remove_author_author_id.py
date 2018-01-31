# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookinfo', '0003_auto_20171205_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='author_id',
        ),
    ]
