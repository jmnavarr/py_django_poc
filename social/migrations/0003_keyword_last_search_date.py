# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20170802_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='last_search_date',
            field=models.DateTimeField(null=True, verbose_name=b'last search date'),
        ),
    ]
