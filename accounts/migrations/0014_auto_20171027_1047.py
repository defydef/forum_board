# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_newskill_profiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newskill',
            name='profiles',
        ),
        migrations.AddField(
            model_name='profile',
            name='newskill',
            field=models.ManyToManyField(to='accounts.NewSkill'),
        ),
    ]
