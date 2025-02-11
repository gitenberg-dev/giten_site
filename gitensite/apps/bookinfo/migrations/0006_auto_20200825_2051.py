# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-08-25 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookinfo', '0005_auto_20180501_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='aliases',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='full_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='gutenberg_bookshelf',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='gutenberg_type',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(db_index=True, default='en', max_length=5),
        ),
        migrations.AlterField(
            model_name='book',
            name='subjects',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(db_index=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='yaml',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='cover',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='bookcovers/'),
        ),
    ]
