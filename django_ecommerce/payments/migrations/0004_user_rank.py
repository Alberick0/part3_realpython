# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0003_unpaidusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rank',
            field=models.CharField(default='Padwan', max_length=50),
        ),
    ]
