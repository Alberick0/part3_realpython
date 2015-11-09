# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20151108_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bigCoID',
            field=models.CharField(default='foo', max_length=50),
            preserve_default=False,
        ),
    ]
