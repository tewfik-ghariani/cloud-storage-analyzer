# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 10:19
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0006_fieldsfdv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldsfdv',
            name='object',
        ),
        migrations.AddField(
            model_name='configobject',
            name='fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='fieldsFDV',
        ),
    ]
