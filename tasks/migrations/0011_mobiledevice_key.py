# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-08 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20160906_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobiledevice',
            name='key',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
