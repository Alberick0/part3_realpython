# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_badge'),
        ('payments', '0004_user_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='badge',
            field=models.ManyToManyField(to='main.Badge'),
        ),
    ]