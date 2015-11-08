# -*- coding utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_default_user(apps, schema_editor):  # two parameters needed
    new_user = apps.get_model('payments', 'User')
    try:
        vader = new_user.objects.get(email='darth@mec.com')
        vader.delete()
    except new_user.DoesNotExist:
        pass

    u = new_user(name='vader', email='darth@mec.com',
                 last_4_digits='1234', password=make_password('pass')).save()


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0005_user_badge'),
    ]

    operations = [
        migrations.RunPython(create_default_user)  # Data migrations
    ]
