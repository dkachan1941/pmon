# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_mobiledevices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobiledevices',
            name='task',
        ),
        migrations.DeleteModel(
            name='MobileDevices',
        ),
    ]
