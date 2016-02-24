# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0002_statusreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True,
                                        serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now=True)),
                ('img', models.CharField(max_length=25, null=True)),
                ('vid', models.URLField(null=True)),
                ('info', models.TextField()),
            ],
        ),
    ]
