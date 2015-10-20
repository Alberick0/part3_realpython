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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('email', models.CharField(unique=True, max_length=100)),
                ('last_notification', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
