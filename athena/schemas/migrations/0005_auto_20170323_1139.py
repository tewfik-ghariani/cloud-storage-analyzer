# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0004_salesschema_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='thdSales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('html_type', models.CharField(max_length=20)),
                ('attribute', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameModel(
            old_name='SalesSchema',
            new_name='testSchema',
        ),
    ]
