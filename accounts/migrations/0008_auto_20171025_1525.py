# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 04:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male')], max_length=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='suburb',
            field=models.CharField(blank=True, choices=[('SUN', 'Sunshine'), ('DP', 'Deer Park'), ('SA', 'St. Albans'), ('SYD', 'Sydenham'), ('ALB', 'Albion')], max_length=3),
        ),
    ]
