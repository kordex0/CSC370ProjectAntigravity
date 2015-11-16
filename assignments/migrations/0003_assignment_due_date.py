# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_auto_20151017_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 16, 4, 44, 21, 378651, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
