# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 03:42
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20171024_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='document',
            field=models.FileField(blank=True, upload_to=accounts.models.user_directory_path),
        ),
    ]
