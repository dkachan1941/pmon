# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-06 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20160906_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='pricefrom',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='priceto',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='quant',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='takephoto',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='article',
            name='unit',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='competitor',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='mobiledevice',
            name='change_password',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='completedate',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
