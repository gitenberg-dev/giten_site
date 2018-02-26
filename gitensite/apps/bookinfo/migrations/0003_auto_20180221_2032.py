# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookinfo', '0002_auto_20160314_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('aliases', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('birth_year', models.IntegerField(null=True)),
                ('death_year', models.IntegerField(null=True)),
                ('wikipedia_url', models.URLField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.URLField(max_length=500)),
                ('default_cover', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='External_Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=500)),
                ('source', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='full_text',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='gutenberg_bookshelf',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AddField(
            model_name='book',
            name='gutenberg_type',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='num_downloads',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='subjects',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_id',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='external_link',
            name='book',
            field=models.ForeignKey(to='bookinfo.Book'),
        ),
        migrations.AddField(
            model_name='cover',
            name='book',
            field=models.ForeignKey(to='bookinfo.Book'),
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(to='bookinfo.Author', null=True),
        ),
    ]
