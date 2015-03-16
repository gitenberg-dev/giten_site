# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Readme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='bookrepo',
            old_name='title',
            new_name='name',
        ),
        migrations.AddField(
            model_name='bookrepo',
            name='clone_url',
            field=models.URLField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookrepo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.utcnow, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookrepo',
            name='open_issues',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bookrepo',
            name='book_id',
            field=models.IntegerField(unique=True, blank=True),
            preserve_default=True,
        ),
    ]
