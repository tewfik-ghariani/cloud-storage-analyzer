# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 09:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configobject',
            name='customer',
        ),
        migrations.DeleteModel(
            name='configObject',
        ),
        migrations.DeleteModel(
            name='s3Info',
        ),
    ]
