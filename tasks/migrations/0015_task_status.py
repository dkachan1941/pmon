# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-08 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20160908_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
    ]