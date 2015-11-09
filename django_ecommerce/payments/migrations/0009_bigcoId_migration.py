# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def migrate_bigcoid(apps, schema_editor):
    user = apps.get_model('payments', 'User')

    for u in user.objects.all():
        bid = (
            '{}{}{}'.format(
                u.name[:2], u.rank[:1],
                u.created_at.strftime('%Y%m%d%H%M%S%f'),
            )
        )

        u.bigCoID = bid
        u.save()


class Migration(migrations.Migration):
    dependencies = [('payments', '0008_user_bigcoid'), ]

    operations = [migrations.RunPython(migrate_bigcoid)]
