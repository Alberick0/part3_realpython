# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_announcements'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True,
                                        verbose_name='ID', serialize=False)),
                ('when', models.DateTimeField(auto_now=True)),
                ('img', models.CharField(max_length=25, null=True)),
                ('vid', models.URLField(blank=True, null=True)),
                ('info', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Announcements',
        ),
    ]
