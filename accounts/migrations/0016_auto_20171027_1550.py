# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 04:50
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20171027_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='newskill2',
        ),
        migrations.AddField(
            model_name='profile',
            name='newskill2',
            field=tagulous.models.fields.SingleTagField(_set_tag_meta=True, blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.TagModel'),
        ),
    ]