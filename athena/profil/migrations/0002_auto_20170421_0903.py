# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 09:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='user',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
