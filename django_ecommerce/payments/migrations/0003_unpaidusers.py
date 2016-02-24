# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0002_auto_20151011_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnPaidUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        verbose_name='ID', serialize=False)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('last_notification', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
