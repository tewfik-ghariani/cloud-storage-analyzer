# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-08 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0014_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='s3Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('shortcut', models.CharField(max_length=20)),
                ('bucket_name', models.CharField(max_length=50, unique=True)),
                ('bucket_region', models.CharField(choices=[('us-east-1', 'us-east-1'), ('us-east-2', 'us-east-2'), ('us-west-1', 'us-west-1'), ('eu-west-1', 'eu-west-1'), ('ap-south-1', 'ap-south-1'), ('ap-northeast-1', 'ap-northeast-1'), ('ap-northeast-2', 'ap-northeast-2'), ('ap-southeast-1', 'ap-southeast-1'), ('ap-southeast-2', 'ap-southeast-2'), ('eu-central-1', 'eu-central-1'), ('eu-west-1', 'eu-west-1'), ('eu-west-2', 'eu-west-2')], max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='test',
        ),
    ]
