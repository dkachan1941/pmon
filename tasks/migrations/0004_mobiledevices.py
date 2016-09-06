# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_competitor_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileDevices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('uuid', models.CharField(max_length=250)),
                ('phone_number', models.CharField(max_length=250, blank=True)),
                ('task', models.ForeignKey(blank=True, to='tasks.Task', null=True)),
            ],
            options={
                'verbose_name': '\u041c\u043e\u0431\u0438\u043b\u044c\u043d\u043e\u0435 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e',
                'verbose_name_plural': '\u041c\u043e\u0431\u0438\u043b\u044c\u043d\u044b\u0435 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430',
            },
            bases=(models.Model,),
        ),
    ]
