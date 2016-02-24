# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0009_bigcoId_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bigCoID',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
