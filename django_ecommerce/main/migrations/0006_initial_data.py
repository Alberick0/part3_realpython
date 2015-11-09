# -*- coding utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations


def create_initial_marketing_item(apps, schema_editor):
    json_data = json.load(open('main/fixtures/system_data.json'))
    MarketingItem = apps.get_model('main', 'MarketingItem')

    for member in json_data:
        new = MarketingItem(
            img=member['fields']['img'],
            heading=member['fields']['heading'],
            caption=member['fields']['caption'],
            button_title=member['fields']['button_title']
        )

        new.save()


class Migration(migrations.Migration):
    dependencies = [('main', '0005_badge'), ]

    operations = [migrations.RunPython(create_initial_marketing_item)]
